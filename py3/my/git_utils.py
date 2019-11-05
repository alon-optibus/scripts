from collections import namedtuple
from datetime import datetime

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


def iter_git_log(path='', n=None):
    import os
    from pathlib import Path

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
