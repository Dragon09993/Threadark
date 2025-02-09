import os
import time
import random
import requests
from minio import Minio
from minio.error import S3Error
import html
import re
from django.utils.safestring import mark_safe

class FourChanApiWrapper:
    BASE_API_URL = "https://a.4cdn.org"
    BASE_IMAGE_URL = "https://i.4cdn.org"

    def __init__(self, board):
        self.board = board

    def get_all_threads(self):
        url = f"{self.BASE_API_URL}/{self.board}/threads.json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    def get_posts_from_thread(self, thread_id):
        url = f"{self.BASE_API_URL}/{self.board}/thread/{thread_id}.json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            
            return False

    def get_catalog(self):
        url = f"{self.BASE_API_URL}/{self.board}/catalog.json"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            response.raise_for_status()

    
    def get_posts_with_urls(self, thread_id):
        thread_data = self.get_posts_from_thread(thread_id)
        thread_data["info"] = {"thread_id": thread_id}
        for post in thread_data["posts"]:
            if "tim" in post and "ext" in post:
                post["image_url"] = f"{self.BASE_IMAGE_URL}/{self.board}/{post['tim']}{post['ext']}"
        return thread_data


    def format_message(self,message,stripHTML=True,linkURLs=False,stripURLs=False):
        url_regex = re.compile(r'(https?:\/\/[^\s|>|<]+)')

        # Unescape HTML entities
        message = html.unescape(message)

        # Remove HTML tags
        if stripHTML:
            message = re.sub(r'<[^>]+>', '', message)
            # Replace '>' with '><br>'
            message = re.sub(r'(?<!>)>(?!>)', ' <br>>', message)
        
        if linkURLs:
            # Strip <wbr> tags
            message = message.replace('<wbr>', '')        
            # Replace URLs with clickable links
            message = url_regex.sub(r' <a target="_blank" href="\1">\1</a> ', message)
        if stripURLs:
            # Strip <wbr> tags
            message = message.replace('<wbr>', '')        
            # Replace URLs with clickable links
            message = url_regex.sub(r'', message)   
                     
        return mark_safe(message)
    
    def format_posts(self, posts):

        for post in posts:
            if 'com' in post:
                post['com'] = self.format_message(post['com'],False,True)

        return posts