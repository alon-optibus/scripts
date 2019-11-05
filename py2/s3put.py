from __future__ import print_function, division

from s3utils import s3_put_file, s3_key_for_file, s3_has, s3_del
from sys import argv
from pathlib2 import Path

########################################################################################################################

if len(argv) == 2:
    path = Path(argv[1]).resolve(True)
    key = s3_key_for_file(path)

else:
    key, path = argv[1:]
    path = Path(path).resolve(True)

if s3_has(key):
    print('s3 del "{}"...'.format(key))
    s3_del(key)

    if s3_has(key):
        print("Faild!")
        quit()

print('s3 put file "{}" in "{}"...'.format(
    path,
    key,
))

s3_put_file(key=key, path=path)

print("Done." if s3_has(key) else "Faild!")

########################################################################################################################
