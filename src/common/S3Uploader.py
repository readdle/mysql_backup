import subprocess
import boto3
import os
import threading
import sys

class ProgressPercentage(object):
    def __init__(self, filename, size):
        self._size = float(size)
        self._seen_so_far = 0
        self._lock = threading.Lock()
    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write("... %s / %s  (%.2f%%)" % 
                            (self._seen_so_far, self._size, percentage))
            if (self._seen_so_far == self._size):
                sys.stdout.write("\n") 
            sys.stdout.flush()



class S3Uploader:
    def __init__(self):
        pass

    @staticmethod
    def upload(path_to_upload, bucket):
        s3 = boto3.client('s3')
        key = os.path.basename(path_to_upload)
        size = os.path.getsize(path_to_upload)
        progress = ProgressPercentage(path_to_upload, size)
        s3.upload_file(path_to_upload, bucket, key, Callback=progress)  
        head_dict = s3.head_object(Bucket=bucket, Key=key)
        if head_dict['ContentLength'] != size: 
            raise Exception('got file in S3 with different size')
