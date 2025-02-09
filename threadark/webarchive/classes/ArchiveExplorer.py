from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from webarchive.models import Thread, Message
from pprint import pprint

class ArchiveExplorer:
    def __init__(self, board):
        self.board = board

    def get_thread_context(self, thread_id):
        try:
            thread = Thread.objects.get(board=self.board, thread_id=thread_id)
            messages = Message.objects.filter(thread_id=thread).order_by('time')
            posts = []
            for message in messages:
                post = {
                    'no': message.message_id,
                    'sub': thread.title,
                    'name': 'Anonymous',  # Assuming all posts are anonymous
                    'now': message.time.strftime('%m/%d/%y(%a)%H:%M:%S'),
                    'com': message.text,
                    'image_url': message.image_url
                }
                posts.append(post)
            context = {
                'board': self.board,
                'thread_id': thread_id,
                'posts': posts
            }
            return context
        except Thread.DoesNotExist:
            return None
        
    def get_all_threads(self, request, pageSize=25):
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort', 'thread_id')

        threads = Thread.objects.filter(board=self.board)

        if search_query:
            threads = threads.filter(
                Q(thread_id__icontains=search_query) |
                Q(board__icontains=search_query) |
                Q(title__icontains=search_query) |
                Q(status__icontains=search_query)
            )

        threads = threads.order_by(sort_by)
        
        page = request.GET.get('page', 1)  # Get page number from URL
        paginator = Paginator(threads, pageSize)  
        
        try:
            threads_page = paginator.page(page)
        except PageNotAnInteger:
                threads_page = paginator.page(1)  # If page is not an integer, show first page
        except EmptyPage:
                threads_page = paginator.page(paginator.num_pages)  # If page is out of range, show last page

        return threads_page