#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

from .options import *

# load sources
from .postgresql import *
from .sqlite import *

class Config:
    @staticmethod
    def init(argv, parser):
        options = Options(argv, parser)

        logging.basicConfig(filename=options.logfile,
            level=options.loglevel,
            format="%(asctime)s %(levelname)s %(filename)s:%(lineno)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")

        logger.info("""
    ###
    ### Exporter called with args: %s
    ###""", options.argv)

        logger.debug("Options: %s", options)

        return options
