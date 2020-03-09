import os
from collections import namedtuple
from datetime import datetime
from pathlib import Path

# <editor-fold desc="utils for git-log">

GitLogCommit = namedtuple(
    'GitLogCommit',
    [
        'date',
        'hash',
        'author',
        'commiter',
        'subject',
        'decoration',
    ]
)

_GIT_LOG__SEP_LINE = '-'*80

_GIT_LOG__DATA_FORMAT_PARTS = [
    '%cI',  # commit date
    '%H',   # hash
    '%an',  # author name
    '%cn',  # commiter name
    '%s',   # subject
    '%D',   # decoration (ref names)
    _GIT_LOG__SEP_LINE,
]

assert len(_GIT_LOG__DATA_FORMAT_PARTS) == len(GitLogCommit._fields) + 1

_GIT_LOG__DATA_FORMAT = '%n'.join(_GIT_LOG__DATA_FORMAT_PARTS)

# </editor-fold>


def get_current_git_branch():
    return os.popen('git rev-parse --abbrev-ref HEAD').read().strip()


def iter_git_log(
        path=None,
        n=None,
        filter_author=None,
        filter_commiter=None,
        filter_merges=False,
):

    if path:
        path = str(Path(path).resolve(True))
        cmd_parts = [f'cd {path};']
    else:
        cmd_parts = []

    cmd_parts.append('git log --decorate=short')

    if n:
        cmd_parts.append(f'-n {n}')

    if filter_author:
        cmd_parts.append(f'--author={filter_author}')

    if filter_commiter:
        cmd_parts.append(f'--committer={filter_commiter}')

    if filter_merges:
        cmd_parts.append('--merges')

    cmd_parts.append(f'--pretty="{_GIT_LOG__DATA_FORMAT}"')

    cmd = ' '.join(cmd_parts)

    raw = iter(os.popen(cmd))

    while True:

        try:
            (
                raw_date,
                hash_,
                author,
                commiter,
                subject,
                decoration,
                split_line,
            ) = (
                next(raw).strip()
                for _ in range(len(_GIT_LOG__DATA_FORMAT_PARTS))
            )

        except RuntimeError:
            return

        assert split_line == _GIT_LOG__SEP_LINE, split_line

        date = datetime.fromisoformat(raw_date)

        yield GitLogCommit(
            date=date,
            hash=hash_,
            author=author,
            commiter=commiter,
            subject=subject,
            decoration=decoration,
        )

    pass


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
