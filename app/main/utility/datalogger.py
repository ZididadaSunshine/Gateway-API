import datetime
import fcntl
import time
from functools import wraps

_current_milli_time = lambda: int(round(time.time() * 1000))


def _format_log_date(date):
    return datetime.datetime.strftime(date, '%Y-%m-%d %H:%M:%S.%f')


def _append_time(category, time):
    file = f'logs/{category}_timer.dat'
    contents = f'{_format_log_date(datetime.datetime.utcnow())}={time}'

    with open(file, 'a') as file:
        fcntl.flock(file, fcntl.LOCK_EX)
        file.write(contents + '\n')
        fcntl.flock(file, fcntl.LOCK_UN)


def log_time(category):
    def wrapper(func):
        def wrapped(*args, **kwargs):
            return _log_time(category, func, *args, **kwargs)

        return wrapped

    return wrapper


def _log_time(category, function, *args, **kwargs):
    now = _current_milli_time()
    ret_value = function(*args, *kwargs)
    _append_time(category, _current_milli_time() - now)

    return ret_value
