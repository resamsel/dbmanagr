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

    def __init__(self, _logger):
        self.logger = _logger

    def __call__(self, f):
        '''Returns a wrapper that wraps f. The wrapper will log the entry
and exit points of the function with logging.DEBUG level.
'''

        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if self.logger.getEffectiveLevel() <= logging.DEBUG:
                fargs = args
                if f.__name__ == '__init__':
                    fargs = fargs[1:]
                fargs = map(
                    lambda (k, v): argtostring(k, v),
                    inspect.getcallargs(f, *fargs).iteritems())
                fargs += map(
                    lambda (k, v): encode(v),
                    kwargs)
                formats = map(lambda arg: '%s', fargs) + map(
                    lambda (k, v): '{}=%s'.format(k), kwargs)
                self.logger.debug(
                    ENTRY_MESSAGE.format(', '.join(formats)),
                    f.__name__, *fargs)
                start = time.time()
                result = f(*args, **kwargs)
                self.logger.debug(
                    EXIT_MESSAGE,
                    f.__name__,
                    (time.time() - start) * 1000.0,
                    encode(result))
                return result
            else:
                return f(*args, **kwargs)
        return wrapper


def logduration(subject, start):
    logger.info('%s took: %0.6fs', subject, time.time() - start)
