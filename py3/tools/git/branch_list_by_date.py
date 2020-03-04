import argparse
from fnmatch import fnmatch

from my.utils.git_1 import get_current_git_branch
from my.utils.git_1 import get_user_name_from_git_config
from my.utils.git_1 import iter_git_branch_by_date


def termfmt(i): return f"\033[{i}m{{}}\033[00m".format

########################################################################################################################

parser = argparse.ArgumentParser(description='list git-branches sorted by last commit date.')

# <editor-fold desc="define arg: number of lines">

parser.add_argument(
    '-n',
    type=int,
    nargs='?',
    help='Number of branches to print. if no value is given, list all.',
    default=10,
)

# </editor-fold>
# <editor-fold desc="define arg: filter by author">

parser.add_argument(
    '-a',
    type=str,
    nargs='?',
    help='filter by author. if no value is given, consider user name from git config.',
    default='*',
    metavar='author',
)

# </editor-fold>

args = parser.parse_args()

if args.a is None:
    args.a = get_user_name_from_git_config()

print(args)

########################################################################################################################

# <editor-fold desc="select branches">

if args.a == '*':

    branches = list(iter_git_branch_by_date(n=args.n))

else:

    branches = []

    for branch_data in iter_git_branch_by_date():
        date, author, branch = branch_data
        if fnmatch(author, args.a):
            branches.append(branch_data)

            if args.n is not None and len(branches) >= args.n:
                break

# </editor-fold>

current_git_branch = get_current_git_branch()

author_width = max(
    len(author)
    for date, author, refname in branches
)

for i, (date, author, branch) in enumerate(branches):

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
