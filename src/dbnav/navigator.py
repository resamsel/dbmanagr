#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import sys
import argparse

from .config import Config
from .item import Item, create_items, create_connections, INVALID
from dbnav.writer import Writer, StdoutWriter, FormatWriter, XmlWriter, TestWriter, SimplifiedWriter
from .sources import Source
from .logger import logger, logduration

IMAGE_CONNECTION = 'images/connection.png'
IMAGE_DATABASE = 'images/database.png'
IMAGE_TABLE = 'images/table.png'

logger = logging.getLogger(__name__)

def strip(s):
    if type(s) == str:
        return s.strip()
    return s

parser = argparse.ArgumentParser(prog='dbnav')
parser.add_argument('uri', help="""the URI to parse (format for PostgreSQL: user@host/database/table/filter; for SQLite: databasefile.db/table/filter)""", nargs='?')
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--default', help='use default writer', action='store_true')
group.add_argument('-s', '--simple', help='use simple writer', action='store_true')
group.add_argument('-j', '--json', help='use JSON writer', action='store_true')
group.add_argument('-x', '--xml', help='use XML writer', action='store_true')
group.add_argument('-a', '--autocomplete', help='use autocomplete writer', action='store_true')
group.add_argument('-t', '--test', help='use test writer', action='store_true')
parser.add_argument('-S', '--simplify', dest='simplify', default=True, help='simplify the output', action='store_true')
parser.add_argument('-N', '--no-simplify', dest='simplify', help='simplify the output', action='store_false')
parser.add_argument('-m', '--limit', type=int, default=50, help='limit the results of the main query to this amount of rows')
parser.add_argument('-f', '--logfile', default='/tmp/dbnavigator.log', help='the file to log to')
parser.add_argument('-l', '--loglevel', default='warning', help='the minimum level to log')

class DatabaseNavigator:
    """The main class"""

    @staticmethod
    def navigate(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.driver)
            if opts.show != 'connections' and connection.matches(opts):
                return connection.proceed(opts)

        # print all connections
        return create_connections(sorted([c for c in cons if c.filter(options)], key=lambda c: c.title().lower()))

def main():
    try:
        print Writer.write(run(sys.argv))
    except SystemExit, e:
        sys.exit(-1)
    except BaseException, e:
        sys.stderr.write('{0}: {1}\n'.format(sys.argv[0].split('/')[-1], e))
        raise

def run(argv):
    options = Config.init(argv, parser)
    if options.simplify:
        Writer.set(SimplifiedWriter())
    if options.xml:
        Writer.set(XmlWriter())
    if options.test:
        Writer.set(TestWriter())

    try:
        return DatabaseNavigator.navigate(options)
    except BaseException, e:
        logger.exception(e)
        return [Item('', str(e), type(e), '', INVALID, '')]

if __name__ == "__main__":
    main()
