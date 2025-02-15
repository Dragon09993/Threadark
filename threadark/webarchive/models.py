from django.db import models

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=5, unique=True)  # Board name (e.g., 'g', 'b', etc.)
    description = models.TextField(null=True, blank=True)  # Description of the board
    active = models.BooleanField(default=False)  # Indicates if the board is active

    def __str__(self):
        return self.name


class Thread(models.Model):
    # Define the fields for the Thread model id (primary), thread_id, thread_title, thread_status, thread_url, created_at
    id = models.AutoField(primary_key=True)
    #thread_id of 4chan thread indexed
    thread_id = models.BigIntegerField() 
    # 4chan board
    board = models.CharField(max_length=5)
    title = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=15, default='open')
    url = models.URLField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    replies = models.IntegerField(default=0)
    response_json = models.JSONField(null=True, blank=True)
    

    class Meta:
        unique_together = ("board", "thread_id")  # Ensure (board, thread_id) is unique
        indexes = [
            models.Index(fields=["board", "thread_id"]),  # Index for fast lookups
        ]

    def __str__(self):
        return self.title
    

class Message(models.Model):
    # Define the fields for the Message model id (primary), thread_id, message_id, message_text, message_time
    id = models.AutoField(primary_key=True)
    board = models.CharField(max_length=5)
    thread_id = models.ForeignKey(Thread, on_delete=models.CASCADE)
    # 4chan message id
    message_id = models.CharField(max_length=50)
    text = models.TextField(null=True, blank=True)
    time = models.DateTimeField()
    # has_audio boolean
    has_audio = models.BooleanField(default=False)
    image_url = models.URLField(max_length=255, null=True, blank=True)
    audio_url = models.URLField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ("board", "thread_id", "message_id")  # Ensure (board, thread_id) is unique
        indexes = [
            models.Index(fields=["board", "thread_id", "message_id"]),  # Index for fast lookups
        ]

    def __str__(self):
        return self.text[:50] if self.text else ''  # Return first 50 characters of the message text or an empty string if text is None