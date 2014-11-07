#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import functools

from dbnav.utils import encode

logger = logging.getLogger(__name__)

ENTRY_MESSAGE = u'⇢ %s({})'
EXIT_MESSAGE = u'⇠ %s [%0.3fms] = %s'


class log_with(object):
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
                fargs = map(encode, fargs) + map(
                    lambda (k, v): encode(v), kwargs)
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
