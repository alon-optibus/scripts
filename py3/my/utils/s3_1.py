import boto3
from pathlib import Path
import os

########################################################################################################################

S3ClientError = boto3.exceptions.botocore.exceptions.ClientError

s3resource = boto3.resource('s3')
s3bucket__algo = s3resource.Bucket('algo-research')

DEFAULT_PREFIX_FOR_FILES = 'alon-misc-files'

PATH_HOME = os.getenv('HOME')

########################################################################################################################


def s3_object_exists(object_):
    try:
        object_.load()
    except S3ClientError as exception_:
        if exception_.response['Error']['Code'] != "404":
            raise
        return False
    else:
        return True


########################################################################################################################


def s3_key_for_file(path):
    path = Path(path).resolve()
    if path.is_dir():
        raise ValueError(f'path is dir: {path}')
    path = str(path).replace(PATH_HOME, '~')
    return '{}:{}'.format(DEFAULT_PREFIX_FOR_FILES, path)


def s3_has(key, bucket=s3bucket__algo):
    return s3_object_exists(bucket.Object(key))


def s3_put_file(key, path, bucket=s3bucket__algo):
    return bucket.Object(key).upload_file(str(path))


def s3_get_file(key, path, bucket=s3bucket__algo):
    return bucket.download_file(key, str(path))


def s3_del(key, bucket=s3bucket__algo):
    return bucket.Object(key).delete()


########################################################################################################################

