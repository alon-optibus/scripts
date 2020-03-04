import argparse
from fnmatch import fnmatch

from my.utils.git_1 import get_user_name_from_git_config
from my.utils.git_1 import iter_git_log

parser = argparse.ArgumentParser(description='Parse and print git log.')

# <editor-fold desc="define arg: number of lines">

parser.add_argument(
    '-n',
    type=int,
    nargs='?',
    help='Number of lines to read from git log. if no value is given, list all.',
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
# <editor-fold desc="define arg: filter merge-commits">

parser.add_argument(
    '-m',
    action='store_true',
    help='filter merge-commits.',
)

# </editor-fold>
# <editor-fold desc="parse args">

args = parser.parse_args()

if args.a is None:
    args.a = get_user_name_from_git_config()

# </editor-fold>
# <editor-fold desc="select commits">

if args.a == '*' and not args.m:

    commits = list(iter_git_log(n=args.n))

else:

    commits = []

    for commit in iter_git_log():

        if (
                (args.a == '*' or fnmatch(commit.author, args.a)) and
                (not args.m or ''.join(commit.desc[:1]).startswith('Merge branch '))
        ):
            commits.append(commit)

            if args.n is not None and len(commits) >= args.n:
                break

# </editor-fold>
# <editor-fold desc="print commits">

author_size = max(
    len(x.author)
    for x in commits
)

for i, x in enumerate(commits):

    desc = ''.join(x.desc[:1])

    print(f'{i:4} : {x.date:%y-%m-%d %H:%M} By {x.author:{author_size}} : {desc}')

# </editor-fold>
########################################################################################################################
