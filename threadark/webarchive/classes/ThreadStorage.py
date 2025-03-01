from minio import Minio
from .FourChanApiWrapper import FourChanApiWrapper
from webarchive.models import Thread
from webarchive.models import Message
import requests
from pprint import pprint
import time
from datetime import datetime
import os
class ThreadStorage:

    def __init__(self, board):
        self.FourChanApiWrapper = FourChanApiWrapper(board)
        self.board = board

    def store_posts(self,thread_id):
        
        #pprint(posts)
        #exit()
        json_response = self.FourChanApiWrapper.get_posts_from_thread(thread_id)
        if not json_response:
            thread = Thread.objects.filter(thread_id=thread_id, board=self.board).first()
            if thread:
                thread.status = 'closed'
                thread.save()
            print(f"Failed to retrieve posts for thread {thread_id}")
            return
        else:
            apiobj = self.FourChanApiWrapper.get_posts_with_urls(thread_id)
            posts= apiobj['posts']
            url = apiobj['info']['url']
            for index, post in enumerate(posts):

                if 'image_url' in post and post['image_url']:
                    minio_url = self.store_image_in_minio(post['image_url'])
                else:
                    minio_url = ''
                if 'sub' not in post:
                    post['sub']=''
                if index == 0:
                    # Perform some action for the first post
                    thread, created = Thread.objects.get_or_create(
                        thread_id=thread_id,
                        defaults={
                            'board': self.board,
                            'title': post['sub'],
                            'url': url,
                            'created_at': datetime.fromtimestamp(post['time']).strftime('%Y-%m-%d %H:%M:%S'),
                            'last_updated': datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'),
                            'response_json': json_response,
                        })
                    if 'archived_on' in post:
                        thread.status = 'archived'
                        
                    if not created:
                        # Update the existing thread if needed
                        thread.title = post['sub']
                        thread.url = url
                        thread.created_at = datetime.fromtimestamp(post['time']).strftime('%Y-%m-%d %H:%M:%S')

                    thread.last_updated = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
                    thread.response_json = json_response
                    thread.replies = post['replies']
                    thread.save()

                # Store post in Django's PostgreSQL database
                message, created = Message.objects.update_or_create(
                    message_id=post['no'],
                    defaults={
                        'thread_id': thread,
                        'text': post.get('com'),
                        'image_url': minio_url,
                        'board': self.board,
                        'time': datetime.fromtimestamp(post['time']).strftime('%Y-%m-%d %H:%M:%S'),
                    }
                )
                if not created:
                    # Update the existing message if needed
                    message.text = post.get('com')
                    message.image_url = minio_url
                    message.save()


    def store_image_in_minio(self, image_url):
        # Download the image and store it in Minio
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            minio_client = Minio(
                endpoint="minio:9000",
                access_key=os.getenv('AWS_ACCESS_KEY_ID'),
                secret_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                secure=False
            )
            object_name = image_url.split('/')[-1]
            bucket_name = os.getenv('AWS_STORAGE_BUCKET_NAME')

            # Check if the object already exists in Minio
            try:
                minio_client.stat_object(bucket_name, object_name)
                # If the object exists, return the existing URL
                return f"http://minio:9000/{bucket_name}/{object_name}"
            except Exception as e:
                try:
                    # If the object does not exist, proceed with the upload
                    minio_client.put_object(
                        bucket_name,
                        object_name,
                        response.raw,
                        length=int(response.headers['Content-Length']),
                        content_type=response.headers['Content-Type']
                    )
                    return f"http://minio:9000/{bucket_name}/{object_name}"
                except Exception as e:
                    print(f"Failed to upload image to Minio: {e}")
        return None