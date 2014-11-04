#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

from .options import *

# load sources
from .postgresql import *
from .sqlite import *
from .mysql import *

class Config:
    @staticmethod
    def init(argv, parser):
        options = Options(map(lambda arg: arg.decode("utf-8"), argv), parser)

        logging.basicConfig(stream=options.logfile,
            level=options.loglevel,
            format="%(asctime)s %(levelname)s %(filename)s:%(lineno)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")

        logger.info("""
###
### %s called with args: %s
###""", parser.prog, options.argv)

        logger.debug("Options: %s", options)

        return options
