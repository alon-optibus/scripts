from __future__ import print_function, division

from s3utils import s3_del, s3_key_for_file, s3_has
from sys import argv

########################################################################################################################

_, path = argv

key = s3_key_for_file(path)

if s3_has(key):
    print('s3 del "{}"...'.format(key))
    s3_del(key)

    print("Faild!" if s3_has(key) else "Done.")

else:
    print('s3 key "{}" not found.'.format(key))

########################################################################################################################
