import os
from collections import namedtuple
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path
from typing import *

from my.utils.bash_1 import shell_lines

ROOT_ARMADA = Path.home().joinpath("dev", "armada")

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

    raw = shell_lines(cmd_parts, path)

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


@dataclass(frozen=True)
class BranchInfo:
    name: str
    author: str
    date: datetime
    local: bool
    path: Path
    root: Path

    def delete_branch(self, *, force=False, verbose=True):

        if self.local:
            return delete_local_git_branch(
                branch_name=self.name,
                cwd=self.root,
                force=force,
                verbose=verbose,
            )

        raise NotImplementedError

    pass


def iter_git_branch_by_date(
        path: Optional[Path]=None,
        n: int=None,
        oldest: bool=False,
) -> Iterator[BranchInfo]:

    cmd_parts = [
        "git for-each-ref",
        "--sort={}committerdate".format('' if oldest else '-'),
        "refs/heads/",
        "--format='%(committerdate:raw)|%(authorname)|%(refname:short)'",
    ]

    root = Path.cwd() if path is None else path

    if n:
        cmd_parts.insert(1, f'--count={n}')

    for line in shell_lines(cmd_parts, path):
        raw_date, author, refname = line.split('|', 2)
        timestamp_str, _ = raw_date.split(' ', 1)
        date = datetime.fromtimestamp(int(timestamp_str))

        yield BranchInfo(
            name=refname,
            author=author,
            date=date,
            local=True,
            path=root.joinpath('.git', 'refs', 'heads', refname),
            root=root,
        )

    pass


def delete_local_git_branch(branch_name, *, cwd=None, force=False, verbose=True):
    return list(shell_lines([
        'git branch',
        '-D' if force else '-d',
        '-v' if verbose else '',
        branch_name,
    ], cwd))


########################################################################################################################


def get_user_name_from_git_config():
    return os.popen('git config user.name').readline().strip()


########################################################################################################################
if __name__ == '__main__':

    for b in iter_git_branch_by_date(
        path=Path.home().joinpath("dev", "armada"),
    ):
        print(b.path, b.path.is_file())
    pass
