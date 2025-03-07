import boto3.session
from decouple import config
import boto3
from django.conf import settings


class Bucket():
    """
    CDN bucker manager
    
    init method create s3 resource
    
    NOTE: none of these methods are async use public interface on tasks.py
    """
    
    def __init__(self):
        session = boto3.session.Session()
        self.connection = session.client(
            service_name='s3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            endpoint_url=config('AWS_S3_ENDPOINT_URL'),
        )

    def get_object_list(self):
        result = self.connection.list_objects_v2(Bucket=config('AWS_STORAGE_BUCKET_NAME'))
        if result['KeyCount']:
            return result['Contents']
        return None

    def delete_object(self, key):
        self.connection.delete_object(Bucket=config('AWS_STORAGE_BUCKET_NAME'), Key=key)
        return True

    def download_object(self, key):
        self.connection.download_file(config('AWS_STORAGE_BUCKET_NAME'), key, settings.AWS_LOCAL_DIRECTORY + key.split('/')[-1])
        return True


bucket = Bucket()