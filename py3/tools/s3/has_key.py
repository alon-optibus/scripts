from my.utils.s3_1 import s3_has
from sys import argv

########################################################################################################################

key,  = argv[1:]

print(int(s3_has(key=key)))

########################################################################################################################
