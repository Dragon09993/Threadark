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
    
    def clean_html_for_tts(self, text):
        """Clean HTML and formatting from text for TTS"""
        if not text:
            return ""
        
        # Decode HTML entities first
        text = html.unescape(text)
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Replace common formatting with spoken equivalents
        text = re.sub(r'&gt;&gt;(\d+)', r'replying to post \1', text)  # >>123 -> "replying to post 123"
        text = re.sub(r'&gt;', '', text)  # Remove greentext arrows
        text = re.sub(r'\n+', '. ', text)  # Replace newlines with periods
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        # Remove or replace other common 4chan formatting
        text = re.sub(r'\[spoiler\].*?\[/spoiler\]', 'spoiler text', text)  # Spoiler tags
        text = re.sub(r'==.*?==', 'red text', text)  # Red text
        
        # Limit length for TTS (optional - very long posts can be problematic)
        if len(text) > 500:
            text = text[:500] + "... message truncated"
        
        return text
    
    def generate_message_audio(self, thread_id, message_id):
        message = Message.objects.filter(thread_id=thread_id, message_id=message_id).first()
        if message.text is None:
            return None
        
        # Clean the text for TTS
        audio_text = self.clean_html_for_tts(message.text)
        
        # Skip if text is empty after cleaning
        if not audio_text or len(audio_text.strip()) < 3:
            return None
        
        if message.has_audio:
            return message.audio_url
        try:
            print(f"Generating TTS for: {audio_text[:100]}...")  # Debug output
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
            
            # Clean up local file
            if os.path.exists(audio_file):
                os.remove(audio_file)
                
            return minio_url
        except Exception as e:
            print(f"Error uploading to MinIO: {e}")
            return None

    def generate_thread_audio(self):
        print(f"Board: {self.board}, Thread ID: {self.thread_id}")
        # Fetch the thread from the database
        thread = Thread.objects.filter(board=self.board, thread_id=self.thread_id).first()
        if not thread:
            print(f"Thread not found for board {self.board} and thread ID {self.thread_id}")
            return

        # Fetch all messages from the thread
        messages = Message.objects.filter(board=self.board, thread_id=thread.id).order_by('time')
        
        if not messages.exists():
            print("No messages found.")
            return
        
        print(f"Processing {messages.count()} messages for TTS...")
        
        # Loop through each message and generate audio
        for message in messages:
            if message.text:  # Only process messages with text
                self.generate_message_audio(thread.id, message.message_id)