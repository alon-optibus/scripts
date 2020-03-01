from sys import argv
from my.utils.git_1 import iter_git_branch_by_date
from my.utils.git_1 import get_current_git_branch

def termfmt(i): return f"\033[{i}m{{}}\033[00m".format

########################################################################################################################

n = 10 if len(argv)==1 else int(argv[1])

########################################################################################################################

data = list(iter_git_branch_by_date(n=n))

current_git_branch = get_current_git_branch()

author_width = max(
    len(author)
    for date, author, refname in data
)

for i, (date, author, branch) in enumerate(data):

    branch: str

    var = f'b{i}'

    if branch == current_git_branch:
        print(termfmt(42)(f'{date} by {author:{author_width}} : {var:>4} = {branch}'))

    elif branch in ['develop', 'hotfix', 'rc', 'master']:
        print(termfmt(96)(f'{date} by {author:{author_width}} : {var:>4} = {branch}'))

    elif branch.startswith('jenkins-ignore-'):
        print(termfmt(95)(f'{date} by {author:{author_width}} : {var:>4} = {branch}'))

    else:
        print(f'{date} by {author:{author_width}} : {var:>4} = {branch}')


########################################################################################################################
