from django.core.management.base import BaseCommand
from webarchive.models import Thread, Message
from transformers import pipeline
import html

class Command(BaseCommand):
    help = "Updates all threads with a generated title based on the first message if no title exists or is blank"

    def handle(self, *args, **kwargs):
        # Load the language model
        summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

        # Fetch distinct boards
        boards = Thread.objects.values_list('board', flat=True).distinct()

        for board in boards:
            # Fetch threads with no title or a blank title for the current board
            threads = Thread.objects.filter(board=board).filter(title__isnull=True) | Thread.objects.filter(board=board).filter(title__exact='')

            for thread in threads:
                # Fetch the first message in the thread for the current board
                first_message = Message.objects.filter(thread_id=thread, board=board).order_by('time').first()
                if first_message:
                    # Decode HTML entities in the text
                    decoded_text = html.unescape(first_message.text)
                    
                    # Generate a title using the first message
                    summary = summarizer(decoded_text, max_length=10, min_length=5, do_sample=False)
                    generated_title = summary[0]['summary_text']

                    # Update the thread title
                    thread.title = generated_title
                    thread.save()

                    self.stdout.write(self.style.SUCCESS(f"Updated thread {thread.thread_id} on board {board} with title: {generated_title}"))
                else:
                    self.stdout.write(self.style.WARNING(f"No messages found for thread {thread.thread_id} on board {board}"))