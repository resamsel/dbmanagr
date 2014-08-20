#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import sys
import argparse
import re

from .config import Config
from .item import Item, INVALID
from .writer import Writer, StdoutWriter
from .sources import Source
from .logger import logger, logduration
from dbnav.querybuilder import QueryFilter
from dbnav.model.databaseconnection import values

parser = argparse.ArgumentParser(prog='dbgraph')
parser.add_argument('uri', help="""The URI to parse. Format for PostgreSQL: user@host/database/table; for SQLite: databasefile.db/table""")
parser.add_argument('-i', '--include', help='Include the specified columns and their foreign rows, if any. Multiple columns can be specified by separating them with a comma (,)')
parser.add_argument('-x', '--exclude', help='Exclude the specified columns')
parser.add_argument('-f', '--logfile', default='/tmp/dbnavigator.log', help='the file to log to')
parser.add_argument('-l', '--loglevel', default='warning', help='the minimum level to log')

def create_fks(table, include, exclude):
    logger.debug('create_fks(table=%s, include=%s, exclude=%s)', table, include, exclude)
    
    result = []
    includes = {}
    if include:
        for key, fk in table.fks.iteritems():
            for i in include:
                c = re.sub('([^\\.]*)\\..*', '\\1', i)
                logger.debug('include table=%s, fk.a.table=%s, include=%s, c=%s', table.name, fk.a.table.name, i, c)
                if fk.a.table.name == c:
                    result += create_fks(fk.a.table, remove_prefix(c, include), remove_prefix(c, exclude))

    return sorted(
        list(set(result + [fk for fk in table.fks.itervalues()])),
        key=lambda fk: fk.a.table.name)

def remove_prefix(prefix, list):
    p = '%s.' % prefix
    return [re.sub('^%s' % p, '', i) for i in list if i.startswith(p)]

class DatabaseGrapher:
    """The main class"""

    @staticmethod
    def export(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.driver)
            if opts.show == 'tables' and connection.matches(opts):
                try:
                    connection.connect(opts.database)
                    table = connection.tables()[opts.table]
                    return [Item('', str(fk), '', '', '', '') for fk in create_fks(table, opts.include, opts.exclude)]
                finally:
                    connection.close()

        raise Exception('Specify the complete URI to a table')

def main():
    Writer.set(StdoutWriter(u'{0}', u'{title}\n'))
    Writer.write(run(sys.argv))

def run(argv):
    options = Config.init(argv, parser)

    try:
        return DatabaseGrapher.export(options)
    except BaseException, e:
        logger.exception(e)
        sys.stderr.write(str(e))

if __name__ == "__main__":
    main()
