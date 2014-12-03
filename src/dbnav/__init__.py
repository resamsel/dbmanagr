#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import logging
import pdb

from dbnav.writer import Writer
from dbnav.logger import logger as log

__all__ = (
    'navigator', 'item', 'writer', 'sources', 'querybuilder', 'logger',
    'options', 'tests'
)
__drivers__ = []

KIND_VALUE = 'value'
KIND_FOREIGN_KEY = 'foreign-key'
KIND_FOREIGN_VALUE = 'foreign-value'

IMAGE_VALUE = 'images/value.png'
IMAGE_FOREIGN_KEY = 'images/foreign-key.png'
IMAGE_FOREIGN_VALUE = 'images/foreign-value.png'

OPTION_URI_SINGLE_ROW_FORMAT = u'%s%s/?%s'
OPTION_URI_MULTIPLE_ROWS_FORMAT = u'%s%s?%s'


class Wrapper:
    def write(self):
        try:
            sys.stdout.write(Writer.write(self.run()))
        except:
            return -1
        return 0

    def run(self):
        try:
            return self.execute()
        except BaseException as e:
            log.exception(e)
            if log.getEffectiveLevel() <= logging.DEBUG:
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
