from __future__ import print_function, division

import boto3
from pathlib2 import Path

########################################################################################################################

S3ClientError = boto3.exceptions.botocore.exceptions.ClientError

s3resource = boto3.resource('s3')
s3bucket__algo = s3resource.Bucket('algo-research')

DEFAULT_PREFIX_FOR_FILES = 'alon-misc-files'

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
    return '{}:{}'.format(DEFAULT_PREFIX_FOR_FILES, Path(path).name)


def s3_has(key, bucket=s3bucket__algo):
    return s3_object_exists(bucket.Object(key))


def s3_put_file(key, path, bucket=s3bucket__algo):
    return bucket.Object(key).upload_file(str(path))


def s3_get_file(key, path, bucket=s3bucket__algo):
    return bucket.download_file(key, str(path))


def s3_del(key, bucket=s3bucket__algo):
    return bucket.Object(key).delete()


########################################################################################################################
