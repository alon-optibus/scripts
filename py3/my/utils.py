import os
import pickle
from pathlib import Path
from itertools import *
from collections import *
from collections.abc import *
from datetime import *

########################################################################################################################

root_dir = Path('/')
home_dir = Path(os.getenv('HOME'))
data_dir = Path('/data')
dev_dir = home_dir / 'dev'

########################################################################################################################


def lprint(lines, **kw):
	for line in lines:
		print(line, **kw)


########################################################################################################################


def is_io(f):
    import io
    return isinstance(f, io.IOBase)


########################################################################################################################


def iter_pickle_file(f):
    if is_io(f):

        try:
            while True:
                yield pickle.load(f)
        except EOFError:
            pass

    else:

        with open(str(f), 'rb') as f_:
            yield from iter_pickle_file(f_)


########################################################################################################################


def iter_json_file(f):
    if is_io(f):

        from json import loads

        for line in f:
            yield loads(line)

    else:

        with open(str(f), 'rb') as f_:
            yield from iter_json_file(f_)


########################################################################################################################


def find_in_iter(iter_, cond=lambda item: bool(item)):
    for index, item in enumerate(iter_):
        if cond(item):
            return index, item

    raise LookupError()


########################################################################################################################


def get_iter_head(iterable, n=1):

    if isinstance(iterable, Iterator):
        head = list(islice(iterable, n))
        return head, chain(head, iterable)

    else:
        return list(islice(iterable, n)), iterable


########################################################################################################################


def df_from_nametuples(nametuples):
    import pandas

    (first,), nametuples = get_iter_head(nametuples)

    return pandas.DataFrame.from_records(nametuples, columns=type(first)._fields)


########################################################################################################################
