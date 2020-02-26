import os
from sys import argv
from my.utils.git_1 import iter_git_branch_by_date

########################################################################################################################

if len(argv) == 1:
    for i, (date, name) in enumerate(iter_git_branch_by_date(n=10)):
        print(f'{date} [{i:3}] {name}')

else:

    i = int(argv[1])

    name = ''

    for date, name in iter_git_branch_by_date(n=i+1):
        pass

    if name:
        cmd = f'git checkout {name}'
        os.system(cmd)

########################################################################################################################
