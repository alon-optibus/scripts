# <editor-fold desc="module">
from pathlib import Path
from datetime import datetime
from datetime import timedelta
from typing import *

from my.utils.git_1 import delete_local_git_branch
from my.utils.git_1 import BranchInfo
from my.utils.git_1 import iter_git_branch_by_date
from my.utils.git_1 import ROOT_ARMADA

now = datetime.now()
DAY = timedelta(days=1)
WEEK = 7 * DAY
MONTH = 30 * DAY
YEAR = 365 * DAY

join = ''.join

# </editor-fold>

ME = 'alon'

last_date_my = now
last_date_myji = now - 0.5 * YEAR
last_date_other = now - 2 * WEEK

ROOT = ROOT_ARMADA

PROTECTED_NAMES = [
    'develop',
    'rc',
    'hotfix',
]

PROTECTED_LABELS = [
    'OS-12637',  # vip--route-group-homogeneity
    'OS-19298',  # trigger-lambda-for-ColGen
    'fix-progress_scope',
    'vip--test-progress-bar',
    'OS-12637',  # vip--route-group-homogeneity
]

DEPRICATED_LABELS = [
    # <editor-fold desc="old">
    'vip--fix-progress_scope',
    'OS-21269',  # vip--balanced-non-circular-depots
    'OS-23415',  # st--add-create-schedule-input-to-colgen-input
    'OS-23347',  # rebuild-the-s3-directory-structure-for-create-schedule-metrics-with-sub-directories
    'OS-19784',  # write-done-in-the-ColGen-IO-directory
    'OS-24429',  # refactor-colgen-runners
    # </editor-fold>
]

# <editor-fold desc="select branches">


def _select_branch(branch: BranchInfo) -> bool:

    if branch.name in PROTECTED_NAMES:
        return False

    for label in DEPRICATED_LABELS:
        if label in branch.name:
            return True

    if branch.author == ME:
        if branch.name.startswith('jenkins-ignore'):
            if branch.date > last_date_myji:
                return False
        elif branch.date > last_date_my:
            return False

    elif branch.date > last_date_other:
        return False

    if branch.name.startswith('jenkins-ignore'):
        return False

    for label in PROTECTED_LABELS:
        if label in branch.name:
            return False

    return True


def select_branches() -> List[BranchInfo]:
    return list(filter(
        _select_branch,
        iter_git_branch_by_date(
                path=ROOT,
                n=0,
                oldest=True,
        ),
    ))


# </editor-fold>
# <editor-fold desc="display selected">


def display_branches(branches: Iterable[BranchInfo]):

    if not branches:
        print('no branch selected.')
        return

    name_len = max(len(branch.name) for branch in branches)

    msg = 'selected branches:{}'.format(join(
        f'\n - {branch.name:<{name_len}} - (last edit: {branch.date} by {branch.author})'
        for branch in branches
    ))

    print(msg)

    pass


# </editor-fold>
# <editor-fold desc="get approval">


def get_approval(selected):

    while selected:

        ans = input('delete?')

        if ans == 'n':
            return False

        if ans == 'y':
            return True


# </editor-fold>
# <editor-fold desc="delete branches">


def delete_branches(branches):
    for branch in branches:
        branch.delete_branch(
            force=True,
        )

    return


# </editor-fold>
# <editor-fold desc="main">


def main():

    selected = select_branches()

    display_branches(selected)

    if get_approval(selected):
        delete_branches(selected)

    pass


# </editor-fold>
if __name__ == '__main__':
    main()
