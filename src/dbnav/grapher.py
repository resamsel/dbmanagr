#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time
import sys
import argparse
import re

from collections import deque
from .config import Config
from .item import Item, INVALID
from .writer import Writer, StdoutWriter
from .sources import Source
from .logger import logger, logduration
from .model.column import Column
from .model.table import Table
from dbnav.utils import prefixes, remove_prefix
from dbnav.querybuilder import QueryFilter
from dbnav.model.databaseconnection import values

PRIMARY_KEY_OPTIONS = {
    True: '*',
    False: ''
}
NULLABLE_OPTIONS = {
    True: '?',
    False: '',
    None: ''
}

DEFAULT_ITEMS_FORMAT = u'{0}'
DEFAULT_ITEM_FORMAT = u'{item}'
GRAPHVIZ_ITEMS_FORMAT = u"""digraph dbgraph {{{0}}}"""
GRAPHVIZ_ITEM_FORMAT = u"""  {fk.a.table.name} -> {fk.b.table.name} [label="{fk.a.name} -> {fk.b.name}"];"""

parser = argparse.ArgumentParser(prog='dbgraph')
parser.add_argument('uri', help="""The URI to parse. Format for PostgreSQL: user@host/database/table; for SQLite: databasefile.db/table""")
group = parser.add_mutually_exclusive_group()
group.add_argument('-d', '--default', default=True, help='Output format: human readable hierarchical text', action='store_true')
group.add_argument('-g', '--graphviz', help='Output format: a Graphviz graph', action='store_true')
parser.add_argument('-c', '--include-columns', default=False, help='Include columns in output (does not work with graphviz as output)', action='store_true')
group = parser.add_mutually_exclusive_group()
group.add_argument('-r', '--recursive', help='Include any forward/back reference to the starting table, recursing through all tables eventually', action='store_true')
group.add_argument('-i', '--include', help='Include the specified columns and their foreign rows, if any. Multiple columns can be specified by separating them with a comma (,)')
parser.add_argument('-x', '--exclude', help='Exclude the specified columns')
parser.add_argument('-f', '--logfile', default='/tmp/dbnavigator.log', help='The file to log to')
parser.add_argument('-l', '--loglevel', default='warning', help='The minimum level to log')

class Node:
    def __init__(self, column, parent=None, fk=None, indent=0):
        self.__dict__['column'] = column
        self.parent = parent
        self.fk = fk
        self.indent = indent
    def escaped(self, f):
        return dict(map(lambda (k, v): (k.encode('ascii', 'ignore'), f(v)), self.__dict__.iteritems()))
    def __getattr__(self, name):
        if self.fk:
            return getattr(self.fk, name)
        if name in self.__dict__:
            return self.__dict__[name]
        return None
    def __repr__(self):
        return self.__str__()
    def __str__(self):
        indent = '  '*self.indent
        if self.fk:
            if self.fk.a.table.name == self.parent.name:
                return '{0}+ {1}{3} -> {2}'.format(indent,
                    self.fk.a.name,
                    self.fk.b,
                    NULLABLE_OPTIONS.get(self.fk.a.nullable))
            return '{0}+ {1} ({2} -> {3})'.format(indent,
                self.fk.a.table.name, self.fk.a.name, self.fk.b.name)
        column = self.__dict__['column']
        return '{0}- {1}{2}{3}'.format(indent,
            column.name,
            PRIMARY_KEY_OPTIONS.get(column.primary_key),
            NULLABLE_OPTIONS.get(column.nullable),
            column.table.name)

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
                result.append(Node(col, table, None, indent))
        elif fk.a.table.name == table.name and fk.b.table.name not in consumed:
            # Collects the forward references
            result.append(Node(fk.b, table, fk, indent))
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
            result.append(Node(fk.a, table, fk, indent))
            if opts.recursive or fk.a.table.name in prefixes(include):
                result += dfs(fk.a.table,
                    consumed,
                    remove_prefix(fk.a.table.name, include),
                    remove_prefix(fk.a.table.name, exclude),
                    indent + 1,
                    opts)

    return result

def bfs(start, consumed=[], include=[], exclude=[], indent=0, opts=None):
    logger.debug('bfs(start=%s, consumed=%s, include=%s, exclude=%s, indent=%d)',
        start, consumed, include, exclude, indent)

    head = [start]
    found = True
    while found:
        found = False
        tail = deque(head)
        head = []

#        logger.debug('found=%s, tail=%s, consumed=%s, indent=%d', found, tail, consumed, indent)

        while tail:
            node = tail.popleft()

            if isinstance(node, Table):
                table = node
                if table.name in consumed:
                    continue

                consumed.append(table.name)
                table.init_columns(table.connection)

                logger.debug('consume table=%s, consumed=%s, indent=%d', table, consumed, indent)

                for col in filter(lambda col: col.name not in exclude, table.cols):
                    fk = table.foreign_key(col.name)
                    if not fk:
                        if opts.include_columns:
                            # Add column
                            head.append(Node(col, table, None, indent))
                    elif fk.a.table.name == table.name and fk.b.table.name not in consumed:
                        # Collects the forward references
                        head.append(Node(fk.b, table, fk, indent))
                        if opts.recursive or fk.a.name in prefixes(include):
                            head.append(fk.b.table)
                            found = True

                for key, fk in filter(
                        lambda (key, fk): fk.b.table.name == table.name and fk.a.table.name not in exclude,
                        table.fks.iteritems()):
                    if fk.a.table.name not in consumed:
                        # Collects the back references
                        head.append(Node(fk.a, table, fk, indent))
                        if opts.recursive or fk.a.table.name in prefixes(include):
                            head.append(fk.a.table)
                            found = True
            else:
                head.append(node)
        indent += 1

    return head

class DatabaseGrapher:
    """The main class"""

    @staticmethod
    def export(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.driver)
            if connection.matches(opts) and opts.show in ['tables', 'columns', 'values']:
                try:
                    connection.connect(opts.database)
                    tables = connection.tables()
                    if  opts.table not in tables:
                        raise Exception("Could not find table '{0}'".format(opts.table))
                    table = tables[opts.table]
                    return [table] + bfs(
                        table,
                        include=opts.include,
                        exclude=opts.exclude,
                        opts=opts)
                finally:
                    connection.close()

        raise Exception('Specify the complete URI to a table')

def main():
    Writer.write(run(sys.argv))

def run(argv):
    options = Config.init(argv, parser)
    if options.default:
        Writer.set(StdoutWriter(DEFAULT_ITEMS_FORMAT, DEFAULT_ITEM_FORMAT))
    if options.graphviz:
        Writer.set(StdoutWriter(GRAPHVIZ_ITEMS_FORMAT, GRAPHVIZ_ITEM_FORMAT))

    try:
        nodes = DatabaseGrapher.export(options)
        return nodes
    except BaseException, e:
        logger.exception(e)
        raise

if __name__ == "__main__":
    main()
