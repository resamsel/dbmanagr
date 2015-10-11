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

from dbmanagr.wrapper import Wrapper
from dbmanagr.config import Config
from dbmanagr.sources.source import Source
from dbmanagr.logger import LogWith
from dbmanagr.utils import find_connection, to_dict, selection, is_included, \
    is_excluded
from dbmanagr.writer import Writer
from dbmanagr.dto.mapper import to_dto
from dbmanagr.exception import UnknownTableException, \
    UnknownConnectionException

from .args import parser
from .writer import GraphWriter, GraphvizWriter
from .node import ColumnNode, ForeignKeyNode, NameNode, TableNode

logger = logging.getLogger(__name__)


def include_forward_references(
        table, head, consumed, include, exclude, indent, opts):
    found = False
    for col in filter(
            lambda col: (
                not is_excluded(col.name, exclude) or
                is_included(col.name, include)),
            table.columns()):
        logger.debug('col.name %s not in exclude %s', col.name, exclude)
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
            if (is_included(fk.a.name, include)
                    or (opts.recursive and fk.b.table.name not in consumed)):
                # logger.debug('adds table=%s', fk.b.table)
                head.append(TableNode(
                    fk.b.table,
                    include=selection(fk.a.name, include),
                    exclude=selection(fk.a.name, exclude),
                    indent=indent + 1))
                found = True

    return found


def include_back_references(
        table, head, consumed, include, exclude, indent, opts):
    found = False
    for _, fk in filter(
            lambda (key, fk): (
                fk.b.table.name == table.name
                and (
                    not is_excluded(fk.a.table.name, exclude)
                    or is_included(fk.a.table.name, include))),
            table.foreign_keys().iteritems()):
        logger.debug(
            'adds back reference: fk=%s, include=%s',
            fk, include)
        head.append(ForeignKeyNode(fk, table, indent))
        if (is_included(fk.a.table.name, include)
                or (opts.recursive and fk.a.table.name not in consumed)):
            # Collects the back references
            # logger.debug('adds table=%s', fk.a.table)
            head.append(TableNode(
                fk.a.table,
                include=selection(fk.a.table.name, include),
                exclude=selection(fk.a.table.name, exclude),
                indent=indent + 1))
            found = True

    return found


def bfs(start, include, exclude, indent, opts):
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
                    continue  # pragma: no cover
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

                if include_forward_references(
                        table, head, consumed, include, exclude, indent, opts):
                    found = True

                logger.debug(
                    'opts.include_back_references: %s',
                    opts.include_back_references)
                if opts.include_back_references and include_back_references(
                        table, head, consumed, include, exclude, indent, opts):
                    found = True
            else:
                head.append(node)
        indent += 1

    return head


class DatabaseGrapher(Wrapper):
    """The main class"""
    def __init__(self, options):
        Wrapper.__init__(self, options)

        if options.formatter:
            Writer.set(options.formatter(options))
        else:
            Writer.set(GraphWriter(options))

    @LogWith(logger)
    def execute(self):
        """The main method that splits the arguments and starts the magic"""
        options = self.options

        # search exact match of connection
        connection, opts = find_connection(
            Source.connections(),
            options,
            lambda con, opts: con.matches(opts))

        if connection is None:
            raise UnknownConnectionException(
                options.uri,
                map(lambda c: c.autocomplete(), Source.connections()))

        if opts.show not in ['tables', 'columns', 'values']:
            raise Exception('Specify the complete URI to a table')

        return to_dto(self.build(connection, opts))

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
                include=to_dict(opts.include),
                exclude=to_dict(opts.exclude),
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


def execute(args):
    """
    Directly calls the execute method and avoids using the wrapper
    """
    return DatabaseGrapher(Config.init(args, parser)).execute()


def run(args):
    return DatabaseGrapher(Config.init(args, parser)).run()


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    return DatabaseGrapher(Config.init(args, parser)).write()
