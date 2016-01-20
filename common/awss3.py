import subprocess


class S3Uploader:
    def __init__(self):
        pass

    @staticmethod
    def upload(path_to_upload, bucket):
        subprocess.call("s3cmd put %s s3://%s/" % (path_to_upload, bucket), shell=True)
        return
