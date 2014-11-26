#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import pdb

from functools import wraps

from dbnav.writer import Writer
from dbnav.logger import logger

__all__ = (
    'navigator', 'item', 'writer', 'sources', 'querybuilder', 'logger',
    'options', 'tests'
)
__drivers__ = []


def decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            print Writer.write(f(*args, **kwargs))
        except (SystemExit, KeyboardInterrupt) as e:
            sys.exit(-1)
        except BaseException as e:
            logger.exception(e)
            if logger.getEffectiveLevel() <= logging.DEBUG:
                # Start post mortem debugging only when debugging is enabled
                if os.getenv('UNITTEST', 'False') == 'True':
                    raise
                type, value, tb = sys.exc_info()
                # traceback.print_exc()
                pdb.post_mortem(tb)
            else:
                # Show the error message if log level is INFO or higher
                sys.stderr.write(
                    '{0}: {1}\n'.format(sys.argv[0].split('/')[-1], e))
    return wrapper
