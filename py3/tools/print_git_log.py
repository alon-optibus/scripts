import argparse
from my.git_utils import iter_git_log

parser = argparse.ArgumentParser(description='Parse and print git log.')

parser.add_argument(
    'n',
    type=int,
    nargs='?',
    help='Number of chars to read from git log.',
    default=10,
)

args = parser.parse_args()


commits = list(iter_git_log(n=args.n))

# desc_size = max(
#     len(x.desc)
#     for x in commits
# )

author_size = max(
    len(x.author)
    for x in commits
)

# now = datetime.now(timezone(datetime.now()-datetime.utcnow()))

for i, x in enumerate(commits):

    desc = ''.join(x.desc[:1])

    print(f'{i:4} : {x.date:%y-%m-%d %H:%M} By {x.author:{author_size}} : {desc}')

    # print(f'{i:4} : {x.date:%y-%m-%d %H:%M} : {x.desc:{desc_size}} : By {x.author}')
    # print(f'{i:4} : {now-x.date} : {x.desc:{desc_size}} : By {x.author}')

########################################################################################################################
