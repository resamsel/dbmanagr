#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import sys
import argparse

from collections import deque, OrderedDict
from dbnav.config import Config
from dbnav.writer import Writer, StdoutWriter
from dbnav.sources import Source
from dbnav.logger import logger, logduration
from dbnav.model.table import Table
from dbnav.utils import prefixes, remove_prefix
from dbnav.querybuilder import QueryFilter
from dbnav.args import parent_parser, format_group

parent = parent_parser()
group = format_group(parent)
group.add_argument('-d', '--default', default=True, help='output format: tuples', action='store_true')
parser = argparse.ArgumentParser(prog='dbexec', parents=[parent])
parser.add_argument('uri', help="""the URI to parse (format for PostgreSQL: user@host/database; for SQLite: databasefile.db)""")
parser.add_argument('infile', default='-', help='the path to the file containing the SQL query to execute', type=argparse.FileType('r'), nargs='?')
parser.add_argument('-s', '--separator', default=';\n', help='the separator between individual statements')

class Item:
    def __init__(self, connection, row):
        self.connection = connection
        self.row = row
    def __str__(self):
        return '\t'.join(map(lambda c: unicode(c), self.row))

class DatabaseExecuter:
    """The main class"""

    @staticmethod
    def execute(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.driver)
            if connection.matches(opts) and opts.show in ['databases', 'tables', 'columns', 'values']:
                try:
                    connection.connect(opts.database)
                    try:
                        sql = opts.infile.readlines()
                    except KeyboardInterrupt:
                        sql = []
                    finally:
                        opts.infile.close()
                    results = []
                    for stmt in filter(lambda s: len(s.strip()) > 0, ''.join(sql).split(opts.separator)):
                        result = connection.execute(stmt)
                        if result.cursor:
                            results.extend(map(lambda row: Item(connection, row), result))
                    return results
                finally:
                    connection.close()

        raise Exception('Specify the complete URI to a table')

def main():
    try:
        print Writer.write(run(sys.argv))
    except SystemExit, e:
        sys.exit(-1)
    except BaseException, e:
        sys.stderr.write('{0}: {1}\n'.format(sys.argv[0].split('/')[-1], e))

def run(argv):
    options = Config.init(argv, parser)
    if options.default:
        Writer.set(StdoutWriter(u'{0}', u'{item}'))
    if options.test:
        Writer.set(TestWriter())

    try:
        return DatabaseExecuter.execute(options)
    except BaseException, e:
        logger.exception(e)
        raise

if __name__ == "__main__":
    main()
