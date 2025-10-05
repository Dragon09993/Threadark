from minio import Minio
import os
from gtts import gTTS
from webarchive.models import Message
from pprint import pprint
from webarchive.models import Thread
import re
import html

class TtsGen:
    def __init__(self, board, thread_id):
        self.board = board
        self.thread_id = thread_id
        
        self.minio_client = Minio(
            endpoint="10.0.0.2:9000",  # Changed from minio:9000
            access_key=os.getenv('AWS_ACCESS_KEY_ID'),
            secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            secure=False
        )
       
        self.tts_engine = gTTS
    
    def generate_message_audio(self, thread_id, message_id):
        message = Message.objects.filter(thread_id=thread_id, message_id=message_id).first()
        if message.text is None:
            return None
        else:
            audio_text = message.text
        
        if message.has_audio:
            return message.audio_url
        try:
            tts = self.tts_engine(text=audio_text, lang='en')
            audio_file = f"{thread_id}_{message_id}.mp3"
            tts.save(audio_file)
        except Exception as e:
            print(f"Error generating TTS: {e}")
            return None

        # Upload the audio file to Minio
        bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME', 'picrels')
        try:
            self.minio_client.fput_object(bucket_name, audio_file, audio_file)
            minio_url = f"http://10.0.0.2:9000/{bucket_name}/{audio_file}"  # Changed from minio:9000
            message.audio_url = minio_url
            message.has_audio = True
            message.save()
            return minio_url
        except Exception as e:
            print(f"Error uploading to MinIO: {e}")
            return None

    def generate_thread_audio(self):
        print(f"Board: {self.board}, Thread ID: {self.thread_id}")
        # Fetch all messages from the thread
        # Fetch the thread from the database
        thread = Thread.objects.filter(board=self.board, thread_id=self.thread_id).first()
        if not thread:
            print(f"Thread not found for board {self.board} and thread ID {self.thread_id}")
            return

        # Fetch all messages from the thread
        messages = Message.objects.filter(board=self.board,thread_id=thread.id).order_by('time')
        pprint(messages)
        if not messages.exists():
            print("No messages found.")
        else:
            pprint(messages)
        # Loop through each message and generate audio
        for message in messages:
            self.generate_message_audio(thread.id,message.message_id)