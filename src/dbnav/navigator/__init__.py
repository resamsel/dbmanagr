#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

from dbnav.logger import LogWith
from dbnav import decorator
from dbnav.config import Config
from dbnav.item import Item
from dbnav.writer import Writer
from dbnav.sources import Source
from .args import parser
from .writer import SimplifiedWriter

logger = logging.getLogger(__name__)

IMAGE_CONNECTION = 'images/connection.png'
IMAGE_DATABASE = 'images/database.png'
IMAGE_TABLE = 'images/table.png'


class DatabaseNavigator:
    """The main class"""

    @staticmethod
    @LogWith(logger, log_result=False)
    def navigate(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.dbs)
            if opts.show != 'connections' and connection.matches(opts):
                return connection.proceed(opts)

        # print all connections
        return map(
            lambda c: c.item(),
            sorted(
                [c for c in cons if c.filter(options)],
                key=lambda c: c.title().lower()))


@decorator
def main():
    return run(sys.argv)


def run(argv):
    options = Config.init(argv, parser)

    if options.formatter:
        Writer.set(options.formatter())
    else:
        Writer.set(SimplifiedWriter())

    try:
        return DatabaseNavigator.navigate(options)
    except BaseException, e:
        if Writer.writer.__class__.__name__ in ['XmlWriter', 'TestWriter']:
            return [Item('', unicode(e), e.__class__, '', False, '')]
        else:
            raise

if __name__ == "__main__":
    main()
