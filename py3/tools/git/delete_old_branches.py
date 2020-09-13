from pathlib import Path
from datetime import datetime
from datetime import timedelta

from my.utils.git_1 import delete_git_branch
from my.utils.git_1 import iter_git_branch_by_date


max_time = timedelta(days=30*6)
now = datetime.now()
cwd = Path.home().joinpath("dev", "armada")

if __name__ == '__main__':
    for date, author, branch_name in iter_git_branch_by_date(
            path=cwd,
            n=0,
            oldest=True,
    ):
        if now - date <= max_time:
            break
        print(f'delete local branch "{branch_name}" (last edit: {date} by {author})')
        delete_git_branch(branch_name, cwd=cwd, force=True)
    pass