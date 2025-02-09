from django.core.management.base import BaseCommand
import datetime
from webarchive.models import Thread
from webarchive.classes.ThreadStorage import ThreadStorage

class Command(BaseCommand):
    help = "Updates all threads"

    def handle(self, *args, **kwargs):
        # Get all unique boards
        boards = Thread.objects.values_list('board', flat=True).distinct()

        for board in boards:
            # Initialize ThreadStorage for the current board
            storage = ThreadStorage(board)
            # Filter threads with status 'open'
            threads = Thread.objects.filter(board=board, status='open')
            
            # Get all threads for the current board
            threads = Thread.objects.filter(board=board)
            
            for thread in threads:

                # Run store_posts method on each thread
                storage.store_posts(thread.thread_id)