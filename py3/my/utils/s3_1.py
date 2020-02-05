import boto3
import botocore
from pathlib import Path
import os

########################################################################################################################


def aws_login():
    os.system('saml2aws login --session-duration=32400')


aws_login()

########################################################################################################################

S3ClientError = botocore.exceptions.ClientError

s3resource = boto3.resource('s3')
s3bucket__algo = s3resource.Bucket('algo-research')

DEFAULT_PREFIX_FOR_FILES = 'alon-misc-files'
S3_KEY_PREFIX_FOR_MIRROR = 'alon-mirror'

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


class S3IOError (IOError):
    pass


class S3GetError (S3IOError):
    pass


class S3PutError (S3IOError):
    pass


class S3DelError (S3IOError):
    pass


########################################################################################################################


def s3_has(key, bucket=s3bucket__algo):
    return s3_object_exists(bucket.Object(key))


def s3_del(key, bucket=s3bucket__algo, log_func=print, validate=True):

    if log_func is not None:
        log_func(f'del s3["{key}"]')

    res = bucket.Object(key).delete()

    if validate and s3_has(key=key, bucket=bucket):
        raise S3DelError(res)

    return res


def put_file_in_s3(key, path, bucket=s3bucket__algo, log_func=print, validate=True):
    path = Path(path).resolve(True)
    exists = s3_has(key=key, bucket=bucket)

    if log_func is not None:
        log_func(f'put file "{path}" in s3["{key}"]' + (' (replacing)' if exists else ''))

    if exists:
        s3_del(key=key, bucket=bucket, log_func=log_func, validate=validate)

    res = bucket.Object(key).upload_file(str(path))

    if validate and not s3_has(key=key, bucket=bucket):
        raise S3PutError(res)

    return res


def get_file_from_s3(key, path, bucket=s3bucket__algo, log_func=print, validate=True):
    path = Path(path).resolve()
    parent: Path = path.parent
    exists = path.exists()

    if log_func is not None:
        log_func(f'get file "{path}" from s3["{key}"]' + (' (replacing)' if exists else ''))

    if exists:
        path.unlink()

        if path.exists():
            raise OSError('faild to remove existing file.')

    elif not parent.exists():
        os.makedirs(str(parent))

    res = bucket.download_file(key, str(path))

    if validate and not path.exists():
        raise S3GetError(res)

    return res


def s3_iter(prefix=None, bucket=s3bucket__algo):
    if prefix:
        yield from bucket.objects.filter(Prefix=prefix)
    else:
        yield from bucket.objects.all()


def s3_clear(prefix, bucket=s3bucket__algo, log_func=print, validate=True):
    for x in s3_iter(prefix=prefix, bucket=bucket):
        s3_del(x.key, log_func=log_func, validate=validate)

########################################################################################################################


def s3_mirror_key(path):
    path = Path(path).resolve()
    if path.is_dir():
        raise ValueError(f'path is dir: {path}')
    path = str(path).replace(PATH_HOME, '~')
    return '{}:{}'.format(S3_KEY_PREFIX_FOR_MIRROR, path)


def s3_mirror_has(path):
    return s3_has(s3_mirror_key(path))


def s3_mirror_put(path):
    return put_file_in_s3(s3_mirror_key(path), path)


def s3_mirror_get(path):
    return get_file_from_s3(s3_mirror_key(path), path)


def s3_mirror_del(path):
    return s3_del(s3_mirror_key(path))


def s3_mirror_iter():
    yield from s3_iter(prefix=S3_KEY_PREFIX_FOR_MIRROR)


########################################################################################################################
if __name__ == '__main__':

    from tempfile import mkstemp

    test_prefix = 'test'

    s3_clear(prefix=test_prefix)

    _, p = mkstemp()
    p = Path(p)
    k = 'test:' + p.stem

    print(p, k)

    in_local = p.exists()
    in_s3 = s3_has(k)

    assert in_local
    assert not in_s3

    put_file_in_s3(key=k, path=p)
    put_file_in_s3(key=k, path=p)
    get_file_from_s3(key=k, path=p)

    s3_clear(prefix=test_prefix)

    pass
########################################################################################################################
