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
import urllib2
import json

from dbnav.writer import Writer
from dbnav import logger as log
from dbnav.jsonable import from_json

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

OPERATORS = {
    '=': lambda c, v: c.__eq__(v),
    '!=': lambda c, v: c.__ne__(v),
    '~': lambda c, v: c.like(v),
    '*': lambda c, v: c.like(v),
    '>': lambda c, v: c.__gt__(v),
    '>=': lambda c, v: c.__ge__(v),
    '<=': lambda c, v: c.__le__(v),
    '<': lambda c, v: c.__lt__(v),
    'in': lambda c, v: c.in_(v),
    ':': lambda c, v: c.in_(v)
}
COMMANDS = {
    'dbdiff': 'differ',
    'dbexec': 'executer',
    'dbexport': 'exporter',
    'dbgraph': 'grapher',
    'dbnav': 'navigator'
}


class Wrapper:
    def __init__(self, options=None):
        self.options = options

    def write(self):
        try:
            sys.stdout.write(Writer.write(self.run()))
        except BaseException as e:
            log.logger.exception(e)
            return -1
        return 0

    def run(self):
        try:
            if self.options is not None and self.options.daemon:
                return self.executer(*sys.argv)
            return self.execute()
        except BaseException as e:
            log.logger.exception(e)
            if log.logger.getEffectiveLevel() <= logging.DEBUG:
                # Start post mortem debugging only when debugging is enabled
                if os.getenv('UNITTEST', 'False') == 'True':
                    raise
                type, value, tb = sys.exc_info()  # pragma: no cover
                # traceback.print_exc()
                pdb.post_mortem(tb)  # pragma: no cover
            else:
                # Show the error message if log level is INFO or higher
                log.log_error(e)  # pragma: no cover

    def executer(self, *args):
        """Execute remotely"""

        options = self.options

        try:
            from dbnav import daemon
            daemon.start_server(options)

            url = 'http://{host}:{port}/{path}'.format(
                host=options.host,
                port=options.port,
                path=COMMANDS[options.prog])
            request = json.dumps(args[1:])

            log.logger.debug('Request to %s:\n%s', url, request)

            response = urllib2.urlopen(url, request)

            r = json.load(response)

            log.logger.debug('Response:\n%s', r)

            return from_json(r)
        except urllib2.HTTPError as e:
            raise from_json(json.load(e))
        except urllib2.URLError as e:
            log.logger.error('Daemon not available: %s', e)
        except BaseException as e:
            log.logger.exception(e)
