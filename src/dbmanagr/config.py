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

import os
import logging

from dbmanagr.logger import logger
from dbmanagr.options import Options
from dbmanagr.utils import unicode_decode

# load sources
from importlib import import_module
import dbmanagr.driver as driver
for mod in driver.__all__:
    import_module('dbmanagr.driver.{0}'.format(mod)).init()


class Config(object):
    @staticmethod
    def init(argv, parser):
        options = Options(unicode_decode(argv), parser)

        logging.basicConfig(
            stream=options.logfile,
            level=options.loglevel,
            format="%(asctime)s %(levelname)s %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")

        logger.info(
            """
###
### %s called with args: %s
###""",
            parser.prog, options.argv)

        logger.debug("Options: %s", options)
        logger.debug(
            "Environment: %s",
            dict(filter(
                lambda (k, v): k.startswith('DBNAV_'),
                os.environ.iteritems())))

        return options
