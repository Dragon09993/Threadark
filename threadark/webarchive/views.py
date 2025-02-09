from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse

from .classes.FourChanApiWrapper import FourChanApiWrapper
from pprint import pprint
from .classes.ThreadStorage import ThreadStorage
from .classes.ArchiveExplorer import ArchiveExplorer

# Create your views here.

def index(request):
    return HttpResponse("Hello, world. You're at the webarchive index.")


def about(request):
        return render(request, 'webarchive/about.html')


@login_required
def view_catalog(request,board):
        
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
                     thread['image_url'] ="#"
                
                complete_catalog.append(thread)
        
        #return HttpResponse(pprint(thread))

        return render(request, 'webarchive/view_catalog.html', {'threads': complete_catalog, 'board': board})

@login_required
def view_live_thread(request, board, thread_id):
    fourchanAPI = FourChanApiWrapper(board)
    thread_data = fourchanAPI.get_posts_with_urls(thread_id)
    posts = fourchanAPI.format_posts(thread_data['posts'])
    #posts = thread_data['posts']
    pprint(posts)
    return render(request, 'webarchive/view_live_thread.html', {'posts': posts, 'board': board, 'thread_id': thread_id})

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
    # Store posts in the database
    # You can implement your own logic here to store the posts in your database
    # For example, you can create a model to store the posts and save them to the database
    return HttpResponse("Posts stored successfully.")


@login_required
def view_archive(request, board, page=1):
    thread_list = []
    explorer = ArchiveExplorer(board)
    threads = explorer.get_all_threads(request)
    pprint(threads)

    return render(request, 'webarchive/view_archive.html', {'threads': threads, 'board': board})
