import argparse
from fnmatch import fnmatch

from my.utils.git_1 import get_user_name_from_git_config
from my.utils.git_1 import iter_git_branch_by_date

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

########################################################################################################################

if args.a == '*':
    for date, author, branch in iter_git_branch_by_date(n=args.n):
        print(branch)

else:

    n = 0

    for date, author, branch in iter_git_branch_by_date():

        if fnmatch(author, args.a):
            print(branch)
            n += 1

            if args.n is not None and n >= args.n:
                break


########################################################################################################################
