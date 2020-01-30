#!ipy3

from sys import argv
from my.utils.logs_1 import *
from my.utils.utils_1 import df_from_nametuples

from pathlib import Path

########################################################################################################################

print(argv)
assert len(argv) > 1, 'missing paths to log files.'

log_paths = [
    Path(arg).resolve(True)
    for arg in argv[1:]
]

logs = [
    list(iter_log_file(path))
    for path in log_paths
]

if len(logs) == 1:
    log = logs[0]

for i, (path, log) in enumerate(zip(log_paths, logs)):
    print(f'\nlog #{i}: {path}\nTotla log time: {log_time(log)}')
    log_time(log)

try:
    import pandas as pd
except ImportError:
    print('Unable to import pandas.')
else:

    dfs = [
        df_from_nametuples(log)
        for log in logs
    ]

    if len(dfs) == 1:
        df = dfs[0]

########################################################################################################################
