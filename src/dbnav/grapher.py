#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import sys
import argparse

from collections import deque
from .config import Config
from .item import Item, INVALID
from .sources import Source
from .logger import logger, logduration
from .model.column import Column
from .model.table import Table
from dbnav.utils import prefixes, remove_prefix
from dbnav.querybuilder import QueryFilter
from dbnav.model.databaseconnection import values
from dbnav.node import BaseNode, ColumnNode, ForeignKeyNode, NameNode, TableNode
from dbnav.formatter import Formatter, DefaultFormatter, TestFormatter
from dbnav.writer import Writer, StdoutWriter, GraphvizWriter, FormatWriter
from dbnav.args import parent_parser, format_group

DEFAULT_ITEMS_FORMAT = u'{0}'
DEFAULT_ITEM_FORMAT = u'{item}'

parent = parent_parser()
group = format_group(parent)
group.add_argument('-d', '--default', default=True, help='output format: human readable hierarchical text', action='store_true')
group.add_argument('-g', '--graphviz', help='output format: a Graphviz graph', action='store_true')
parser = argparse.ArgumentParser(prog='dbgraph', parents=[parent])
parser.add_argument('uri', help="""the URI to parse (format for PostgreSQL: user@host/database/table; for SQLite: databasefile.db/table)""")
parser.add_argument('-c', '--include-columns', default=False, help='include columns in output', action='store_true')
parser.add_argument('-D', '--include-driver', default=False, help='include database driver in output (does not work well with graphviz as output)', action='store_true')
parser.add_argument('-C', '--include-connection', default=False, help='include connection in output (does not work well with graphviz as output)', action='store_true')
parser.add_argument('-B', '--include-database', default=False, help='include database in output (does not work well with graphviz as output)', action='store_true')
group = parser.add_mutually_exclusive_group()
group.add_argument('-r', '--recursive', help='include any forward/back reference to the starting table, recursing through all tables eventually', action='store_true')
group.add_argument('-i', '--include', help='include the specified columns and their foreign rows, if any. Multiple columns can be specified by separating them with a comma (,)')
parser.add_argument('-x', '--exclude', help='exclude the specified columns')

def dfs(table, consumed=[], include=[], exclude=[], indent=0, opts=None):
    logger.debug('dfs(table=%s, consumed=%s, include=%s, exclude=%s, indent=%d)',
        table, consumed, include, exclude, indent)

    result=[]
    consumed.append(table.name)
    table.init_columns(table.connection)

    for col in filter(lambda col: col.name not in exclude, table.cols):
        fk = table.foreign_key(col.name)
        if not fk:
            if opts.include_columns:
                # Add column
                result.append(ColumnNode(col, indent))
        elif fk.a.table.name == table.name and fk.b.table.name not in consumed:
            # Collects the forward references
            result.append(ForeignKeyNode(fk, table, indent))
            if opts.recursive or fk.a.name in prefixes(include):
                result += dfs(fk.b.table,
                    consumed,
                    remove_prefix(fk.a.name, include),
                    remove_prefix(fk.a.name, exclude),
                    indent + 1,
                    opts)

    for key, fk in filter(
            lambda (key, fk): fk.b.table.name == table.name and fk.a.table.name not in exclude,
            table.fks.iteritems()):
        if fk.a.table.name not in consumed:
            # Collects the back references
            result.append(ForeignKeyNode(fk, table, indent))
            if opts.recursive or fk.a.table.name in prefixes(include):
                result += dfs(fk.a.table,
                    consumed,
                    remove_prefix(fk.a.table.name, include),
                    remove_prefix(fk.a.table.name, exclude),
                    indent + 1,
                    opts)

    return result

def bfs(start, include=[], exclude=[], indent=0, opts=None):
    logger.debug('bfs(start=%s, include=%s, exclude=%s, indent=%d)',
        start, include, exclude, indent)

    head = [TableNode(start, include, exclude)]
    consumed=[]
    found = True
    while found:
        found = False
        tail = deque(head)
        head = []

        while tail:
            node = tail.popleft()

            if isinstance(node, TableNode):
                table = node.table
                if opts.recursive and table.name in consumed:
                    continue

                include = node.include
                exclude = node.exclude

                consumed.append(table.name)
                table.init_columns(table.connection)

                logger.debug('consume table=%s ,include=%s, exclude=%s, consumed=%s, indent=%d', table, include, exclude, consumed, indent)

                for col in filter(lambda col: col.name not in exclude, table.cols):
                    fk = table.foreign_key(col.name)
#                    logger.debug('consumed=%s', consumed)
                    if not fk:
                        if opts.include_columns:
                            # Add column
                            head.append(ColumnNode(col, indent))
                    elif fk.a.table.name == table.name:
                        # Collects the forward references
                        logger.debug('adds forward reference: fk=%s, include=%s', fk, include)
                        head.append(ForeignKeyNode(fk, table, indent))
                        if (fk.a.name in prefixes(include)
                                or (opts.recursive and fk.b.table.name not in consumed)):
#                            logger.debug('adds table=%s', fk.b.table)
                            head.append(TableNode(fk.b.table,
                                include=remove_prefix(fk.a.name, include),
                                exclude=remove_prefix(fk.a.name, exclude)))
                            found = True

                for key, fk in filter(
                        lambda (key, fk): fk.b.table.name == table.name and fk.a.table.name not in exclude,
                        table.fks.iteritems()):
                    logger.debug('adds back reference: fk=%s, include=%s', fk, include)
                    head.append(ForeignKeyNode(fk, table, indent))
                    if (fk.a.table.name in prefixes(include)
                            or (opts.recursive and fk.a.table.name not in consumed)):
                        # Collects the back references
#                        logger.debug('adds table=%s', fk.a.table)
                        head.append(TableNode(fk.a.table,
                            include=remove_prefix(fk.a.table.name, include),
                            exclude=remove_prefix(fk.a.table.name, exclude)))
                        found = True
            else:
                head.append(node)
        indent += 1

    return head

class DatabaseGrapher:
    """The main class"""

    @staticmethod
    def graph(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.driver)
            if connection.matches(opts) and opts.show in ['tables', 'columns', 'values']:
                try:
                    connection.connect(opts.database)
                    tables = connection.tables()
                    if opts.table not in tables:
                        raise Exception("Could not find table '{0}'".format(opts.table))
                    table = tables[opts.table]
                    nodes = []
                    indent = 0
                    if opts.include_driver:
                        nodes.append(NameNode(connection.driver, indent=indent))
                        indent += 1
                    if opts.include_connection:
                        nodes.append(NameNode(str(connection), indent=indent))
                        indent += 1
                    if opts.include_database and opts.database:
                        nodes.append(NameNode(opts.database, indent=indent))
                        indent += 1
                    nodes.append(NameNode(table.name, indent=indent))
                    nodes += bfs(
                        table,
                        include=opts.include,
                        exclude=opts.exclude,
                        indent=indent,
                        opts=opts)
                    return nodes
                finally:
                    connection.close()

        raise Exception('Specify the complete URI to a table')

def main():
    try:
        print Writer.write(run(sys.argv))
    except SystemExit, e:
        sys.exit(-1)
    except BaseException, e:
        sys.stderr.write('{0}: {1}{2}\n'.format(sys.argv[0].split('/')[-1], e, type(e)))
#        raise

def run(argv):
    options = Config.init(argv, parser)
    if options.default:
        Formatter.set(DefaultFormatter())
        Writer.set(StdoutWriter(DEFAULT_ITEMS_FORMAT, DEFAULT_ITEM_FORMAT))
    if options.graphviz:
        Writer.set(GraphvizWriter())
    if options.test:
        Formatter.set(DefaultFormatter())
        Writer.set(StdoutWriter(DEFAULT_ITEMS_FORMAT, DEFAULT_ITEM_FORMAT))

    try:
        return DatabaseGrapher.graph(options)
    except BaseException, e:
        logger.exception(e)
        raise

if __name__ == "__main__":
    main()
