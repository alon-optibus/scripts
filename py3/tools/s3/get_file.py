from my.utils.s3_1 import s3_get_file, s3_key_for_file
from sys import argv
from pathlib import Path

########################################################################################################################

if len(argv) == 2:
    path = Path(argv[1])
    key = s3_key_for_file(path)

else:
    key, path = argv[1:]
    path = Path(path)


if path.exists():

    print('remove file "{}"...'.format(path))

    path.unlink()

    if path.exists():
        print("Faild!")
        quit()


print('s3 get file{} "{}" from "{}"...'.format(
    ' (replacing)' if path.exists() else '',
    path,
    key,
))

s3_get_file(key=key, path=path)

print("Done." if path.exists() else "Faild!")

########################################################################################################################
