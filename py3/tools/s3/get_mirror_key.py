from my.utils.s3_1 import s3_mirror_key
from sys import argv

########################################################################################################################

path,  = argv[1:]
key = s3_mirror_key(path)

print(key)

########################################################################################################################
