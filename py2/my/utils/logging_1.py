from __future__ import division, print_function

from os import getpid
from threading import RLock, Thread

from psutil import Process
from time import sleep, time

from my.utils import MISSING, NamespaceClass, unmissing_strict

########################################################################################################################


current_pid = getpid()
current_process = Process(current_pid)


def get_process_memory(process=current_process):
    return process.memory_info().rss


def get_process_memory_by_pid(pid=current_pid):
    return get_process_memory(Process(current_pid))


########################################################################################################################


class ContextLogger (object):
    # <editor-fold desc="class variables">

    progress_lock = RLock()

    __slots__ = (
        'label',
        'log_func',
        'log_param',
        'progress_log_interval',
        'enter_time',
        'enter_memory',
        'exit_time',
        'exit_memory',
        'enter_fmt',
        'exit_fmt',
        'progress_fmt',
        'progress_default_fmt',
        'time_fmt',
        'memory_fmt',
        'time_factor',
        'time_unit',
        'memory_factor',
        'memory_unit',
        'process',
        'time',
        '__in_progress',
        '__progress_control_thread',
        '__progress_log_error',
        '__progress_log_index',
    )

    # </editor-fold>
    # <editor-fold desc="main defaults">

    DEFAULT_LABEL = ''
    DEFAULT_PROGRESS_LOG_INTERVAL = 10  # s
    DEFAULT_LOG_FUNC = print

    # </editor-fold>
    # <editor-fold desc="default fmt">

    DEFAULT_ENTER_FMT = '>>>> {label}'
    DEFAULT_PROGRESS_FMT = ':::: {label}: memory={memory}, time={time}'
    DEFAULT_EXIT_FMT = '<<<< {label}: memory={memory}, time={time}'
    DEFAULT_MEMORY_FMT = DEFAULT_TIME_FMT = '{value:>7,.2g}{unit}'
    DEFAULT_PROGRESS_DEFAULT_FMT = DEFAULT_PROGRESS_FMT + ', progress_log_error={progress_log_error!r}'

    # </editor-fold>
    # <editor-fold desc="units">

    class MemoryUnit (NamespaceClass):
        GB = 'GB'
        MB = 'MB'
        KB = 'KB'
        B = 'B'

    class MemoryFactor (NamespaceClass):
        GB = float(2**30)
        MB = float(2**20)
        KB = float(2**10)
        B = 1.

    class TimeUnit (NamespaceClass):
        hr = 'hr'
        m = 'm'
        s = 's'
        ms = 'ms'
        ns = 'ns'

    class TimeFactor (NamespaceClass):
        hr = 3600.
        m = 60.
        s = 1.
        ms = 1e-3
        ns = 1e-6

    DEFAULT_TIME_UNIT = TimeUnit.s
    DEFAULT_MEMORY_UNIT = MemoryUnit.MB

    DEFAULT_TIME_FACTOR = None
    DEFAULT_MEMORY_FACTOR = None

    # </editor-fold>
    # <editor-fold desc="constructors">

    def __init__(
            self,
            label=MISSING,
            log_func=MISSING,
            progress_log_interval=MISSING,
            time_unit=MISSING,
            time_factor=MISSING,
            memory_unit=MISSING,
            memory_factor=MISSING,
            enter_fmt=MISSING,
            exit_fmt=MISSING,
            progress_fmt=MISSING,
            progress_default_fmt=MISSING,
            time_fmt=MISSING,
            memory_fmt=MISSING,
            process=current_process,
            time=time,
            log_param=(),
    ):

        self.label = unmissing_strict(label, self.DEFAULT_LABEL)
        self.log_func = unmissing_strict(log_func, self.DEFAULT_LOG_FUNC)
        self.process = process
        self.time = time
        self.time_fmt = unmissing_strict(time_fmt, self.DEFAULT_TIME_FMT)
        self.memory_fmt = unmissing_strict(memory_fmt, self.DEFAULT_MEMORY_FMT)
        self.enter_fmt = unmissing_strict(enter_fmt, self.DEFAULT_ENTER_FMT)
        self.exit_fmt = unmissing_strict(exit_fmt, self.DEFAULT_EXIT_FMT)
        self.progress_log_interval = unmissing_strict(progress_log_interval, self.DEFAULT_PROGRESS_LOG_INTERVAL)
        self.progress_fmt = unmissing_strict(progress_fmt, self.DEFAULT_PROGRESS_FMT)
        self.progress_default_fmt = unmissing_strict(progress_default_fmt, self.DEFAULT_PROGRESS_DEFAULT_FMT)

        self.log_param = log_param

        self._clear_progress_info()

        time_unit = unmissing_strict(time_unit, self.DEFAULT_TIME_UNIT)
        time_factor = unmissing_strict(time_factor, self.DEFAULT_TIME_FACTOR)

        if time_factor is None:
            self.set_time_unit(time_unit)
        else:
            self.time_factor = time_factor
            self.time_unit = time_unit

        memory_unit = unmissing_strict(memory_unit, self.DEFAULT_MEMORY_UNIT)
        memory_factor = unmissing_strict(memory_factor, self.DEFAULT_MEMORY_FACTOR)

        if memory_factor is None:
            self.set_memory_unit(memory_unit)
        else:
            self.memory_factor = memory_factor
            self.memory_unit = memory_unit

        self.init_param()

        pass

    # </editor-fold>
    # <editor-fold desc="context manager">

    def __enter__(self):
        self._clear_progress_info()

        if self.progress_log_interval is not None:
            self.__progress_control_thread = self._get_progress_control_thread()

        self._log_enter()
        self.__in_progress = True

        if self.__progress_control_thread is not None:
            self.__progress_log_index = -1
            self.__progress_control_thread.start()

        self.enter_memory = self.get_memory()
        self.enter_time = self.get_time()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit_time = self.get_time()
        self.exit_memory = self.get_memory()
        self.__in_progress = False
        self._log_exit()
        pass

    # </editor-fold>
    # <editor-fold desc="time">

    def set_time_unit(self, unit):
        self.time_factor = getattr(self.TimeFactor, unit)
        self.time_unit = unit

    def get_time(self):
        return self.time()

    def get_time_delta(self, cur=None, ref=None):

        if ref is None:
            ref = self.enter_time

        if ref is None:
            return None

        if cur is None:
            cur = self.get_time()

        return cur - ref

    def get_time_str(self, cur=None, ref=None):

        value = self.get_time_delta(cur=cur, ref=ref)

        if value is None:
            return ''

        return self.time_fmt.format(
            value=float(value)/self.time_factor,
            unit=self.time_unit,
        )

    # </editor-fold>
    # <editor-fold desc="memory">

    def set_memory_unit(self, unit):
        self.memory_factor = getattr(self.MemoryFactor, unit)
        self.memory_unit = unit

    def get_memory(self):
        return self.process.memory_info().rss

    def get_memory_delta(self, cur=None, ref=None):

        if ref is None:
            ref = self.enter_memory

        if ref is None:
            return None

        if cur is None:
            cur = self.get_memory()

        return cur - ref

    def get_memory_str(self, cur=None, ref=None):
        value = self.get_memory_delta(cur=cur, ref=ref)

        if value is None:
            return ''

        return self.memory_fmt.format(
            value=float(value)/self.memory_factor,
            unit=self.memory_unit,
        )

    # </editor-fold>
    # <editor-fold desc="progress">

    @property
    def in_progress(self):
        return self.__in_progress

    @property
    def progress_control_thread(self):
        return self.__progress_control_thread

    @property
    def progress_log_error(self):
        return self.__progress_log_error

    @property
    def progress_log_index(self):
        return self.__progress_log_index

    def _progress_control(self):

        sleep(self.progress_log_interval)

        while self.__in_progress:

            with self.progress_lock:

                self.__progress_log_error = None
                self.__progress_log_index += 1

                try:
                    self._log_progress()

                except Exception as e:
                    self.__progress_log_error = e
                    self._log_progress_default()

            sleep(self.progress_log_interval)

    def _get_progress_control_thread(self):

        thread = self.__progress_control_thread = Thread(
            target=self._progress_control,
            name=self._get_progress_control_thread_name(),
        )

        thread.daemon = True

        return thread

    def _get_progress_control_thread_name(self):
        return '{}({!r})'.format(type(self).__name__, self.label)

    def _clear_progress_info(self):
        self.enter_time = None
        self.enter_memory = None
        self.exit_time = None
        self.exit_memory = None
        self.__in_progress = False
        self.__progress_control_thread = None
        self.__progress_log_error = None
        self.__progress_log_index = None

    # </editor-fold>
    # <editor-fold desc="log">

    def format(self, fmt):
        return fmt.format(**self.get_param())

    def _log_enter(self):
        return self.log(self.format(fmt=self.enter_fmt))

    def _log_exit(self):
        return self.log(self.format(fmt=self.exit_fmt))

    def _log_progress(self):
        return self.log(self.format(fmt=self.progress_fmt))

    def _log_progress_default(self):
        return self.log(self.format(fmt=self.progress_default_fmt))

    def log(self, msg):
        return self.log_func(msg)

    # </editor-fold>
    # <editor-fold desc="parameters for log">

    def init_param(self):
        pass

    def get_default_param(self):
        return dict(
            time=self.get_time_str(),
            memory=self.get_memory_str(),
            label=self.label,
            process=self.process,
            progress_log_error=self.__progress_log_error,
            progress_log_index=self.__progress_log_index,
        )

    def get_param(self):
        param = self.get_default_param()
        param.update(self.log_param)
        return param

    # </editor-fold>
    pass


########################################################################################################################
