from my.utils.s3_1 import s3_mirror_key
from sys import argv
from pathlib import Path

########################################################################################################################

if len(argv) == 2:
    path = argv[1]
    key = s3_mirror_key(path)

else:
    key, path = argv[1:]

path = Path(path).resolve()

print(f'venv; aws_login; aws s3 cp "s3://algo-research/{key}" "{path}"')

########################################################################################################################
