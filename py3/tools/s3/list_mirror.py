from my.utils.s3_1 import s3_iter, S3_KEY_PREFIX_FOR_MIRROR
from sys import argv

########################################################################################################################

if len(argv) > 1:
    prefix,  = argv[1:]
else:
    prefix = ''

for x in s3_iter(prefix=S3_KEY_PREFIX_FOR_MIRROR+prefix):
    print(x.key)

########################################################################################################################
