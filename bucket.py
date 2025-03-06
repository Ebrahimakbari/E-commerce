import boto3.session
from decouple import config
import boto3


class Bucket():
    """
    CDN bucker manager
    
    init method create connection
    """
    
    def __init__(self):
        session = boto3.session.Session()
        self.connection = session.client(
            service_name='s3',
            aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
            endpoint_url=config('AWS_S3_ENDPOINT_URL'),
        )