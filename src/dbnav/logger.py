#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import functools
import inspect

logger = logging.getLogger(__name__)

ENTRY_MESSAGE = u'⇢ %s({})'
EXIT_MESSAGE = u'⇠ %s [%0.3fms] = %s'


def encode(v):
    if v is None:
        return None
    if type(v) is unicode:
        return v
    if type(v) is str:
        return unicode(v, 'UTF-8')
    if type(v) is list:
        return map(encode, v)
    return unicode(v)


def argtostring(k, v):
    if k == 'self':
        return k
    return '{0}={1}'.format(k, encode(v))


class LogWith(object):
    '''Logging decorator that allows you to log with a specific logger.
'''

    def __init__(self, logger, log_args=True, log_result=True):
        self.logger = logger
        self.log_args = log_args
        self.log_result = log_result

    def __call__(self, f):
        '''Returns a wrapper that wraps function f. The wrapper will log the
entry and exit points of the function with logging.DEBUG level.
'''

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if self.logger.getEffectiveLevel() <= logging.DEBUG:
                if self.log_args:
                    # Keeps order of args intact
                    cargs = inspect.getcallargs(f, *args)
                    fargs = map(
                        lambda k: argtostring(k, cargs[k]),
                        inspect.getargspec(f).args)
                    # Adds keyword arguments
                    fargs += map(lambda (k, v): encode(v), kwargs)

                    # Creates format for the log message
                    formats = map(lambda arg: '%s', fargs)
                    formats += map(lambda (k, v): '{}=%s'.format(k), kwargs)

                    # Do the logging
                    self.logger.debug(
                        ENTRY_MESSAGE.format(', '.join(formats)),
                        f.__name__, *fargs)
                else:
                    # Do the logging
                    self.logger.debug(
                        ENTRY_MESSAGE.format('<omitted>'),
                        f.__name__)

                # Starts the stopwatch
                start = time.time()
                # Invokes the method/function
                result = f(*args, **kwargs)

                if self.log_result:
                    # Logs returned value and duration of the call
                    self.logger.debug(
                        EXIT_MESSAGE,
                        f.__name__,
                        (time.time() - start) * 1000.0,
                        encode(result))
                else:
                    self.logger.debug(
                        EXIT_MESSAGE,
                        f.__name__,
                        (time.time() - start) * 1000.0,
                        '<omitted>')

                return result
            else:
                return f(*args, **kwargs)
        return wrapper


def logduration(subject, start):
    logger.info('%s took: %0.6fs', subject, time.time() - start)
