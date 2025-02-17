from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django_htmx.http import HttpResponseClientRedirect
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings
import uuid  # Add this import

from .classes.FourChanApiWrapper import FourChanApiWrapper
from pprint import pprint
from .classes.ThreadStorage import ThreadStorage
from .classes.ArchiveExplorer import ArchiveExplorer
from .classes.TtsGen import TtsGen
from .forms import UserRegisterForm, TwoFactorForm
from .models import TwoFactorCode, User

# Create your views here.

def index(request):
    return render(request, 'webarchive/index.html')


def about(request):
    return render(request, 'webarchive/about.html')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserRegisterForm()
    return render(request, 'webarchive/register.html', {'form': form})


@login_required
def view_catalog(request, board):
    complete_catalog = []
    fourchanAPI = FourChanApiWrapper(board)
    catalog = fourchanAPI.get_catalog()
    for page in catalog:
        for thread in page['threads']:
            thread['com'] = fourchanAPI.format_message(thread.get('com', ''))
            thread['sub'] = fourchanAPI.format_message(thread.get('sub', ''))
            if 'tim' in thread and 'ext' in thread:
                thread['image_url'] = f"https://i.4cdn.org/{board}/{thread['tim']}{thread['ext']}"
            else:
                thread['image_url'] = "#"

            complete_catalog.append(thread)

    return render(request, 'webarchive/view_catalog.html', {'threads': complete_catalog, 'board': board})


@login_required
def view_live_thread(request, board, thread_id):
    explorer = ArchiveExplorer(board)
    is_archived = explorer.thread_exists(thread_id)
    fourchanAPI = FourChanApiWrapper(board)
    thread_data = fourchanAPI.get_posts_with_urls(thread_id)
    posts = fourchanAPI.format_posts(thread_data['posts'])
    return render(request, 'webarchive/view_live_thread.html', {'posts': posts, 'board': board, 'thread_id': thread_id, 'is_archived': is_archived})


@login_required
def view_thread(request, board, thread_id):
    explorer = ArchiveExplorer(board)
    context = explorer.get_thread_context(thread_id)
    if context is None:
        return HttpResponse("Thread not found.", status=404)
    posts = context['posts']
    return render(request, 'webarchive/view_thread.html', {'posts': posts, 'board': board, 'thread_id': thread_id})


@login_required
def store_posts(request, board, thread_id):
    storage_obj = ThreadStorage(board)
    storage_obj.store_posts(thread_id)
    return HttpResponse("Posts stored successfully.")

@login_required
def archive_data(request, board):
    explorer = ArchiveExplorer(board)
    threads_pages,threads,paginator = explorer.get_all_threads(request)

    data = {
        "last_page": paginator.num_pages,
        "page": request.GET.get('page', 1),
        "data": [
            {
                "id": thread.id,
                "thread_id": thread.thread_id,
                "board": thread.board,
                "title": thread.title,
                "status": thread.status,
                "url": thread.url,
                "replies": thread.replies,
                "created_at": thread.created_at,
                "last_updated": thread.last_updated
            }
            for thread in threads_pages.object_list
        ]
    }
    return JsonResponse(data)

@login_required
def view_archive(request, board, page=1):
    explorer = ArchiveExplorer(board)
    threads = explorer.get_all_threads(request)

    return render(request, 'webarchive/view_archive.html', {'threads': threads, 'board': board})

@login_required
def tts_audio(request, board, thread_id):
        tts_generator = TtsGen(board, thread_id)
        tts_generator.generate_thread_audio()
        return HttpResponse("Audio generated successfully.")


def custom_logout(request):
    print("Logout function called!")  # Debugging
    logout(request)
    return redirect('login')  # Redirect to login page

def send_2fa_code(user):
    code, created = TwoFactorCode.objects.get_or_create(user=user)
    if not created:
        code.code = uuid.uuid4()
        code.created_at = timezone.now()
        code.save()
    send_mail(
        'Your 2FA Code',
        f'Your verification code is {code.code}',
        'from@example.com',
        [user.email],
        fail_silently=False,
    )

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if request.session.get('remember_device') == user.id:
                login(request, user)
                return redirect('index')
            send_2fa_code(user)
            request.session['pre_2fa_user_id'] = user.id
            return redirect('two_factor')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def two_factor_view(request):
    if request.method == 'POST':
        form = TwoFactorForm(request.POST)
        if form.is_valid():
            user_id = request.session.get('pre_2fa_user_id')
            user = User.objects.get(id=user_id)
            code = form.cleaned_data['code']
            if TwoFactorCode.objects.filter(user=user, code=code).exists():
                login(request, user)
                remember_device = form.cleaned_data.get('remember_device', False)
                if remember_device:
                    request.session['remember_device'] = user.id
                    request.session.set_expiry(2592000)  # 30 days
                else:
                    request.session.set_expiry(0)  # Browser session
                return redirect('index')
    else:
        form = TwoFactorForm()
    return render(request, 'registration/two_factor.html', {'form': form})