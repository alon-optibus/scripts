import os
from sys import argv
from my.utils.git_1 import iter_git_branch_by_date

########################################################################################################################

i = int(argv[1])

name = ''

for date, author, name in iter_git_branch_by_date(n=i+1):
    pass

if name:
    cmd = f'git checkout {name}'
    os.system(cmd)

########################################################################################################################
