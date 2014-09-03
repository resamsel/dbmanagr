#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import sys
import argparse

from dbnav import wrapper
from dbnav.config import Config
from dbnav.item import Item, create_connections, INVALID
from dbnav.writer import Writer, TestWriter
from dbnav.sources import Source
from dbnav.logger import logger
from dbnav.args import parent_parser, format_group

from .writer import SimplifiedWriter, XmlWriter, JsonWriter, SimpleWriter, AutocompleteWriter

IMAGE_CONNECTION = 'images/connection.png'
IMAGE_DATABASE = 'images/database.png'
IMAGE_TABLE = 'images/table.png'

logger = logging.getLogger(__name__)

parent = parent_parser()
group = format_group(parent)
group.add_argument('-d', '--default', help='output format: default', action='store_true')
group.add_argument('-s', '--simple', help='output format: simple', action='store_true')
group.add_argument('-j', '--json', help='output format: JSON', action='store_true')
group.add_argument('-x', '--xml', help='output format: XML', action='store_true')
group.add_argument('-a', '--autocomplete', help='output format: autocomplete', action='store_true')
parser = argparse.ArgumentParser(prog='dbnav', parents=[parent])
parser.add_argument('uri', help="""the URI to parse (format for PostgreSQL: user@host/database/table/filter; for SQLite: databasefile.db/table/filter)""", nargs='?')
parser.add_argument('-S', '--simplify', dest='simplify', default=True, help='simplify the output', action='store_true')
parser.add_argument('-N', '--no-simplify', dest='simplify', help='don\'t simplify the output', action='store_false')
parser.add_argument('-m', '--limit', type=int, default=50, help='limit the results of the main query to this amount of rows')

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
    wrapper(run)

def run(argv):
    options = Config.init(argv, parser)
    if options.simplify:
        Writer.set(SimplifiedWriter())
    if options.xml:
        Writer.set(XmlWriter())
    if options.json:
        Writer.set(JsonWriter())
    if options.simple:
        Writer.set(SimpleWriter())
    if options.autocomplete:
        Writer.set(AutocompleteWriter())
    if options.test:
        Writer.set(TestWriter())

    try:
        return DatabaseNavigator.navigate(options)
    except BaseException, e:
        logger.exception(e)
        return [Item('', str(e), type(e), '', INVALID, '')]

if __name__ == "__main__":
    main()
