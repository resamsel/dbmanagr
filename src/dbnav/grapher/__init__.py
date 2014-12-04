#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

import sys
import logging

from collections import deque

from dbnav import Wrapper
from dbnav.config import Config
from dbnav.sources import Source
from dbnav.logger import LogWith
from dbnav.utils import prefixes, remove_prefix
from dbnav.node import ColumnNode, ForeignKeyNode, NameNode, TableNode
from dbnav.writer import Writer
from dbnav.exception import UnknownTableException

from .args import parser
from .writer import GraphWriter, GraphvizWriter

logger = logging.getLogger(__name__)


def bfs(start, include=[], exclude=[], indent=0, opts=None):
    logger.debug(
        'bfs(start=%s, include=%s, exclude=%s, indent=%d)',
        start, include, exclude, indent)

    head = [TableNode(start, include, exclude, indent)]
    consumed = []
    found = True
    while found:
        if opts.max_depth > 0 and indent > opts.max_depth:
            break

        found = False
        tail = deque(head)
        head = []

        while tail:
            node = tail.popleft()

            if isinstance(node, TableNode) and node.indent >= indent:
                # consume node
                table = node.table
                if opts.recursive and table.name in consumed:
                    continue
                if opts.formatter is GraphvizWriter:
                    # Keep node as we need to display its columns in the graph
                    head.append(node)

                include = node.include
                exclude = node.exclude

                consumed.append(table.name)

                logger.debug(
                    'consume table=%s, include=%s, exclude=%s, consumed=%s, '
                    'indent=%d',
                    table, include, exclude, consumed, indent)

                for col in filter(
                        lambda col: col.name not in exclude, table.columns()):
                    fk = table.foreign_key(col.name)
                    # logger.debug('consumed=%s', consumed)
                    if not fk:
                        if opts.include_columns:
                            # Add column
                            head.append(ColumnNode(col, indent))
                    elif fk.a.table.name == table.name:
                        # Collects the forward references
                        logger.debug(
                            'adds forward reference: fk=%s, include=%s',
                            fk, include)
                        head.append(ForeignKeyNode(fk, table, indent))
                        if (fk.a.name in prefixes(include)
                                or (opts.recursive
                                    and fk.b.table.name not in consumed)):
                            # logger.debug('adds table=%s', fk.b.table)
                            head.append(TableNode(
                                fk.b.table,
                                include=remove_prefix(fk.a.name, include),
                                exclude=remove_prefix(fk.a.name, exclude),
                                indent=indent + 1))
                            found = True

                if opts.include_back_references:
                    for key, fk in filter(
                            lambda (key, fk): (
                                fk.b.table.name == table.name
                                and fk.a.table.name not in exclude),
                            table.fks.iteritems()):
                        logger.debug(
                            'adds back reference: fk=%s, include=%s',
                            fk, include)
                        head.append(ForeignKeyNode(fk, table, indent))
                        if (fk.a.table.name in prefixes(include)
                                or (opts.recursive
                                    and fk.a.table.name not in consumed)):
                            # Collects the back references
                            # logger.debug('adds table=%s', fk.a.table)
                            head.append(TableNode(
                                fk.a.table,
                                include=remove_prefix(
                                    fk.a.table.name, include),
                                exclude=remove_prefix(
                                    fk.a.table.name, exclude),
                                indent=indent + 1))
                            found = True
            else:
                head.append(node)
        indent += 1

    return head


class DatabaseGrapher(Wrapper):
    """The main class"""
    def __init__(self, options):
        self.options = options

        if options.formatter:
            Writer.set(options.formatter(options))
        else:
            Writer.set(GraphWriter(options))

    @LogWith(logger)
    def execute(self):
        """The main method that splits the arguments and starts the magic"""
        options = self.options

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.dbms)
            if connection.matches(opts) and opts.show in [
                    'tables', 'columns', 'values']:
                return self.build(connection, opts)

        raise Exception('Specify the complete URI to a table')

    @LogWith(logger)
    def build(self, connection, opts):
        try:
            connection.connect(opts.database)
            tables = connection.tables()
            if opts.table not in tables:
                raise UnknownTableException(opts.table, tables.keys())
            table = tables[opts.table]
            nodes = []
            indent = 0
            if opts.include_driver:
                nodes.append(
                    NameNode(connection.dbms, indent=indent))
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

            def include_node(item):
                if opts.formatter is GraphvizWriter:
                    if isinstance(item, TableNode):
                        return True
                    if isinstance(item, ColumnNode):
                        return False
                elif opts.include_columns and isinstance(
                        item, ColumnNode):
                    return True
                return not isinstance(item, TableNode)

            return filter(include_node, nodes)
        finally:
            connection.close()


def run(args):
    grapher = DatabaseGrapher(Config.init(args, parser))
    return grapher.run()


def main():
    grapher = DatabaseGrapher(Config.init(sys.argv[1:], parser))
    return grapher.write()
