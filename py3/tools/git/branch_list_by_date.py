# <editor-fold desc="">
import argparse
from fnmatch import fnmatch
from typing import *

from my.utils.bash_1 import termfmt_cf
from my.utils.bash_1 import termfmt_grb
from my.utils.bash_1 import termfmt_pf
from my.utils.git_1 import get_current_git_branch
from my.utils.git_1 import get_user_name_from_git_config
from my.utils.git_1 import iter_git_branch_by_date

# </editor-fold>
# <editor-fold desc="get args">


def get_args() -> argparse.Namespace:

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

    return args


# </editor-fold>
# <editor-fold desc="select branches">


def select_branches(args: argparse.Namespace):

    if args.a == '*':

        branches = list(iter_git_branch_by_date(n=args.n))

    else:

        branches = []

        for branch in iter_git_branch_by_date():
            if fnmatch(branch.author, args.a):
                branches.append(branch)

                if args.n is not None and len(branches) >= args.n:
                    break
    return branches


# </editor-fold>
# <editor-fold desc="main">


def main():

    args: argparse.Namespace = get_args()

    current_git_branch = get_current_git_branch()

    branches = select_branches(args)

    author_width = max(
        len(branch.author)
        for branch in branches
    )

    for i, branch in enumerate(branches):

        var = f'b{i}'
        msg = f'{branch.date} by {branch.author:{author_width}} : {var:>4} = {branch.name}'

        if branch == current_git_branch:
            msg = termfmt_grb(msg)

        if branch in ['develop', 'hotfix', 'rc', 'master']:
            msg = termfmt_cf(msg)

        elif branch.name.startswith('jenkins-ignore-'):
            msg = termfmt_pf(msg)

        print(msg)


# </editor-fold>

if __name__ == '__main__':
    main()
