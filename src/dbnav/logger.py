# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
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
        return repr(v)
    if type(v) is str:
        return encode(unicode(v, 'UTF-8'))
    if type(v) is list:
        return map(encode, v)
    return encode(unicode(v))


def argtostring(k, v):
    if k == 'self':
        return k
    return '{0}={1}'.format(k, encode(v))


def log_error(e):
    sys.stderr.write('{0}: {1}\n'.format(
        sys.argv[0].split('/')[-1], e))


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


class LogTimer(object):
    def __init__(self, logger, subject, prolog=None, *pargs):
        self.logger = logger
        self.subject = subject
        self.start = time.time()
        if prolog is not None:
            self.logger.info(prolog, *pargs)

    def stop(self):
        self.logger.info(
            '%s took: %0.6fs',
            self.subject,
            time.time() - self.start)
