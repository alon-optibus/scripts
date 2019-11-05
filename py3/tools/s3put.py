from my.s3_utils import s3_put_file, s3_key_for_file, s3_has, s3_del
from sys import argv
from pathlib import Path

########################################################################################################################

if len(argv) == 2:
    path = Path(argv[1]).resolve(True)
    key = s3_key_for_file(path)

else:
    key, path = argv[1:]
    path = Path(path).resolve(True)

if s3_has(key):
    print(f's3 del "{key}"...')
    s3_del(key)

    if s3_has(key):
        print("Faild!")
        quit()

print(f's3 put file "{path}" in "{key}"...')

s3_put_file(key=key, path=path)

print("Done." if s3_has(key) else "Faild!")

########################################################################################################################
