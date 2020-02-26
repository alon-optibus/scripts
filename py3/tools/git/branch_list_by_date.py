from sys import argv
from my.utils.git_1 import iter_git_branch_by_date

n = None if len(argv)==1 else int(argv[1])

for i, (date, name) in enumerate(iter_git_branch_by_date(n=n)):
    print(f'{date} [{i:3}] {name}')

########################################################################################################################
