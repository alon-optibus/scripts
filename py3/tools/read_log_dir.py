import os
import json
from pathlib import Path
from datetime import datetime

from statsmodels.genmod.families.links import log

from my.utils.logs_1 import *

########################################################################################################################

dir_path = Path('/data/vip_tests/benchmark_logs/logs_2020-03-09_20-13/').resolve(True)


def get_file_head(path, n=10):
    return os.popen(f'head -n {n} {path!s}')


def get_file_tail(path, n=10):
    return os.popen(f'tail -n {n} {path!s}')


def get_log_line_time(line):
    return datetime.fromisoformat(json.loads(line)['asctime'])


def get_log_file_start_time(path):
    return get_log_line_time(get_file_head(path, 1).readline())


def get_log_file_end_time(path):
    return get_log_line_time(get_file_tail(path, 1).readline())


log_files = [
    (
        get_log_file_start_time(path),
        get_log_file_end_time(path),
        path
    )
    for path in dir_path.iterdir()
]

log_files.sort()

for start, end, path in log_files:
    print(path, start, end)

########################################################################################################################
