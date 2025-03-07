from bucket import bucket
from celery import shared_task


# TODO: can be async?
def get_bucket_list():
    result = bucket.get_object_list()
    return result

@shared_task
def delete_obj_bucket(key):
    result = bucket.delete_object(key)
    return result

@shared_task
def download_obj_bucket(key):
    result = bucket.download_object(key)
    return result