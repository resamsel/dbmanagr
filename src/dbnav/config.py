#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from dbnav.logger import logger
from dbnav.options import Options
from dbnav.utils import unicode_decode

# load sources
import dbnav.sqlite as sqlite
import dbnav.postgresql as postgresql
import dbnav.mysql as mysql

sqlite.init()
postgresql.init()
mysql.init()


class Config:
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

        return options
