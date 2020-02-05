from my.utils.s3_1 import get_file_from_s3, s3_mirror_key
from sys import argv

########################################################################################################################

if len(argv) == 2:
    path = argv[1]
    key = s3_mirror_key(path)

else:
    key, path = argv[1:]

get_file_from_s3(key=key, path=path)

########################################################################################################################
