from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django_htmx.http import HttpResponseClientRedirect

from .classes.FourChanApiWrapper import FourChanApiWrapper
from pprint import pprint
from .classes.ThreadStorage import ThreadStorage
from .classes.ArchiveExplorer import ArchiveExplorer
from .classes.TtsGen import TtsGen

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the webarchive index.")


def about(request):
    return render(request, 'webarchive/about.html')


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
