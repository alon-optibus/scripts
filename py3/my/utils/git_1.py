import os
from collections import namedtuple
from datetime import datetime
from pathlib import Path

GitLogCommit = namedtuple(
    'Commit',
    [
        'id',
        'author',
        'author_mail',
        'date',
        'desc',
        'merge',
    ]
)


def get_current_git_branch():
    return os.popen('git rev-parse --abbrev-ref HEAD').read().strip()


def iter_git_log(path='', n=None):

    cmd = 'git log' if n is None else f'git log -n {n}'

    if path:

        path = str(Path(path).resolve(True))

        raw = os.popen(f'cd {path}; ' + cmd).read()

    else:

        raw = os.popen(cmd).read()

    if not raw.startswith('commit '):
        return None

    logs = raw.split('\ncommit ')
    logs[0] = logs[0][7:]

    for i, log in enumerate(logs):
        author = None
        date = None
        merge = None
        author_mail = None
        desc = []

        id_, *log_lines = log.splitlines()

        for line in log_lines:

            line = line.strip()

            if not line:
                continue

            elif line.startswith('Author: '):
                author, author_mail = line[8:].split(' <')
                author_mail = author_mail[:-1]

            elif line.startswith('Date:   '):
                date = datetime.strptime(line, 'Date:   %a %b %d %H:%M:%S %Y %z')

            elif line.startswith('Merge: '):
                date = line[7:]

            else:
                desc.append(line)

        yield GitLogCommit(
            id=id_,
            author=author,
            date=date,
            merge=merge,
            desc=desc,
            author_mail=author_mail,
        )


def iter_git_branch_by_date(path=None, n=None):

    cmd_parts = [
        "git for-each-ref",
        "--sort=-committerdate refs/heads/ --format='%(committerdate:raw)|%(authorname)|%(refname:short)'"
    ]

    if n:
        cmd_parts.insert(1, f'--count={n}')

    if path:
        cmd_parts.insert(0, f'cd {path};')

    cmd = ' '.join(cmd_parts)

    raw: str = os.popen(cmd).read()

    for line in raw.splitlines(False):
        raw_date, author, refname = line.split('|', 2)
        timestamp_str, _ = raw_date.split(' ', 1)
        date = datetime.fromtimestamp(int(timestamp_str))
        yield date, author, refname

    pass


########################################################################################################################


def get_user_name_from_git_config():
    return os.popen('git config user.name').readline().strip()


########################################################################################################################
