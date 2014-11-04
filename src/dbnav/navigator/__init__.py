#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import argparse

from dbnav import wrapper
from dbnav.config import Config
from dbnav.item import Item
from dbnav.writer import Writer
from dbnav.sources import Source
from dbnav.args import parent_parser, format_group

from .writer import SimplifiedWriter, XmlWriter, JsonWriter, SimpleWriter, AutocompleteWriter

IMAGE_CONNECTION = 'images/connection.png'
IMAGE_DATABASE = 'images/database.png'
IMAGE_TABLE = 'images/table.png'

logger = logging.getLogger(__name__)

parent = parent_parser()
group = format_group(parent)
group.add_argument('-D',
    '--default',
    help='output format: default',
    dest='formatter',
    action='store_const',
    const=SimplifiedWriter)
group.add_argument('-S',
    '--simple',
    help='output format: simple',
    dest='formatter',
    action='store_const',
    const=SimpleWriter)
group.add_argument('-J',
    '--json',
    help='output format: JSON',
    dest='formatter',
    action='store_const',
    const=JsonWriter)
group.add_argument('-X',
    '--xml',
    help='output format: XML',
    dest='formatter',
    action='store_const',
    const=XmlWriter)
group.add_argument('-A',
    '--autocomplete',
    help='output format: autocomplete',
    dest='formatter',
    action='store_const',
    const=AutocompleteWriter)
parser = argparse.ArgumentParser(
    prog='dbnav',
    description='A database navigation tool that shows database structure and'
                ' content',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    parents=[parent])
parser.add_argument('uri',
    help="""the URI to parse (format for PostgreSQL/MySQL: '
        'user@host/database/table?filter; for SQLite: '
        'databasefile.db/table?filter)""",
    nargs='?')
parser.add_argument('-s',
    '--simplify',
    dest='simplify',
    default=True,
    help='simplify the output',
    action='store_true')
parser.add_argument('-N',
    '--no-simplify',
    dest='simplify',
    help='don\'t simplify the output',
    action='store_false')
parser.add_argument('-m',
    '--limit',
    type=int,
    default=50,
    help='limit the results of the main query to this amount of rows')


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
        return map(
            lambda c: c.item(),
            sorted([c for c in cons if c.filter(options)], key=lambda c: c.title().lower()))


def main():
    wrapper(run)


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
