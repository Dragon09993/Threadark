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
            endpoint="minio:9000",
            access_key=os.getenv('AWS_ACCESS_KEY_ID'),
            secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            secure=False
        )
       
        self.tts_engine = gTTS
    
    def generate_message_audio(self, thread_id_id, message_id):
        # Fetch the message from the database
        message = Message.objects.filter(thread_id=thread_id_id, message_id=message_id).first()
        text = re.sub(r'>{2}\d+', '',re.sub(r'<[^>]+>', '', html.unescape(message.text)))
        if message.has_audio:
            print(f"Audio already exists for message {message_id}")
            return
        try:
            # Generate audio from text using gTTS
            tts = gTTS(text=text, lang='en')
            audio_file = f"{self.board}-{self.thread_id}-{message_id}.mp3"
            tts.save(audio_file)
        except Exception as e:
            print(f"Failed to generate audio for message {message_id}: {e}")
            return

        # Upload the audio file to Minio
        bucket_name = 'tts-audio'
        self.minio_client.fput_object(bucket_name, audio_file, audio_file)

        # Generate the Minio URL
        minio_url = f"http://minio:9000/{bucket_name}/{audio_file}"
        message.has_audio = True
        # Update the message model with the audio URL
        message.audio_url = minio_url
        message.save()

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