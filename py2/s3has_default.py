from __future__ import print_function, division

from s3utils import s3_has, s3_key_for_file
from sys import argv

########################################################################################################################

_, path = argv

print(s3_has(s3_key_for_file(path)))

########################################################################################################################
