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
