#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

from dbnav.writer import Writer
from dbnav.logger import logger

__all__ = ('navigator', 'item', 'writer', 'sources', 'querybuilder', 'logger', 'options', 'tests')

def wrapper(f):
    try:
        print Writer.write(f(sys.argv))
    except (SystemExit, KeyboardInterrupt) as e:
        sys.exit(-1)
    except BaseException as e:
        logger.exception(e)
        if logger.getEffectiveLevel() <= logging.DEBUG:
            # Only raise the exception when debugging is enabled!
            raise
        else:
            # Show the error message if log level is INFO or higher
            sys.stderr.write('{0}: {1}\n'.format(sys.argv[0].split('/')[-1], e))
