from collections import namedtuple
from my.utils.utils_1 import iter_json_file
from datetime import datetime


# @attr.s(slots=True, frozen=True)
# class LogLine (object):
#     time = attr.ib()
#     levelname = attr.ib()
#     message = attr.ib()


LogLine = namedtuple(
    'LogLine',
    [
        'time',
        'levelname',
        'message',
        'name',
        'project_id',
        'celeryTaskId',
        'taskId',
        'customer',
        'user',
        'operationType',
        'process',
    ],
)


def iter_log_file(f):
    for line in iter_json_file(f):
        yield LogLine(
            time=datetime.strptime(line.get('asctime'), '%Y-%m-%d %H:%M:%S.%f'),
            levelname=line.get('levelname'),
            message=line.get('message'),
            name=line.get('name'),
            project_id=line.get('project_id'),
            celeryTaskId=line.get('celeryTaskId'),
            taskId=line.get('taskId'),
            customer=line.get('customer'),
            user=line.get('user'),
            operationType=line.get('operationType'),
            process=line.get('process'),
        )


def log_time(log):
    return log[-1].time - log[0].time


def print_log(log):

    name_size = max(len(x.name) for x in log)

    for x in log:

        print(
            f'> {x.time}',
            f'p:{x.process:<5}',
            f'{x.name:{name_size}}',
            f'{x.levelname:7}',
            f'{x.message}',
            sep=' - ',
        )


########################################################################################################################
