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

def create_fks(table, include, exclude, indent=0):
    """Collects columns of that table and foreign keys that point to it"""

    logger.debug('create_fks(table=%s, include=%s, exclude=%s)', table, include, exclude)
    
    result = []
    table.init_columns(table.connection)

    # Collects the columns
    for col in filter(lambda col: col.name not in exclude, table.cols):
        fk = table.foreign_key(col.name)
        result.append(Node(col.name, table, fk, indent))
        for i in filter(lambda name: fk and fk.a.name == name, prefixes(include)):
            result += create_fks(fk.b.table,
                remove_prefix(i, include),
                remove_prefix(i, exclude),
                indent + 1)

    # Collects foreign keys that point to this table
    for key, fk in filter(
            lambda (key, fk): fk.b.table.name == table.name and fk.a.table.name not in exclude,
            table.fks.iteritems()):
        result.append(Node(col.name, table, fk, indent))
        for i in filter(lambda name: fk.a.table.name == name, prefixes(include)):
            result += create_fks(fk.a.table,
                remove_prefix(col.name, include),
                remove_prefix(col.name, exclude),
                indent + 1)
    
    return result

def prefixes(items):
    return set([re.sub('([^\\.]*)\\..*', '\\1', i) for i in items])

def remove_prefix(prefix, items):
    p = '%s.' % prefix
    return [re.sub('^%s' % p, '', i) for i in items if i.startswith(p)]

class Node:
    def __init__(self, name, parent=None, fk=None, indent=0):
        self.__dict__['name'] = name
        self.parent = parent
        self.fk = fk
        self.indent = indent
    def __getattr__(self, name):
        return getattr(self.fk, name)
    def __str__(self):
        indent = '  '*self.indent
        if self.fk:
            if self.fk.a.table.name == self.parent.name:
                return '{0}+ {1} -> {2}'.format(indent,
                    self.fk.a.name,
                    self.fk.b)
            return '{0}+ {1} ({2} -> {3})'.format(indent,
                self.fk.a.table.name, self.fk.a.name, self.fk.b.name)
        return '{0}- {1}'.format(indent, self.__dict__['name'])

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
                    return [Item('', table.name, '', '', '', '')] + [Item('', str(fk), '', '', '', '') for fk in create_fks(table, opts.include, opts.exclude)]
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
