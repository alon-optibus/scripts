import argparse

from my.utils.bash_1 import termfmt_pf
from my.utils.bash_1 import termfmt_rb
from my.utils.git_1 import get_user_name_from_git_config
from my.utils.git_1 import iter_git_log

user_name_from_git_config = get_user_name_from_git_config()

########################################################################################################################

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
    default='',
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
    args.a = user_name_from_git_config

# </editor-fold>
# <editor-fold desc="select commits">

commits = list(iter_git_log(
    n=args.n,
    filter_author=args.a,
    filter_merges=args.m,
))

# </editor-fold>
# <editor-fold desc="print commits">

author_size = max(
    len(x.author)
    for x in commits
)

subject_size = max(
    len(x.subject)
    for x in commits
)

for i, x in enumerate(commits):

    msg = f'{x.date:%y-%m-%d %H:%M} By {x.author:{author_size}} : {x.subject:{subject_size}}'

    if x.decoration:
        msg += f' ({x.decoration})'

    if x.author != user_name_from_git_config:
        msg = termfmt_pf(msg)

    if x.subject.startswith('wip'):
        msg = termfmt_rb(msg)

    print(msg)

# </editor-fold>
########################################################################################################################
