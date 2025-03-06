from bucket import bucket


# TODO: can be async?
def get_bucket_list():
    result = bucket.get_object_list()
    return result