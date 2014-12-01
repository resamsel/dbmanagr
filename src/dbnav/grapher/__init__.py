#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging

from collections import deque

from dbnav import decorator
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


class DatabaseGrapher:
    """The main class"""

    @staticmethod
    @LogWith(logger)
    def graph(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.dbms)
            if connection.matches(opts) and opts.show in [
                    'tables', 'columns', 'values']:
                return DatabaseGrapher.build(connection, opts)

        raise Exception('Specify the complete URI to a table')

    @staticmethod
    @LogWith(logger)
    def build(connection, opts):
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


@decorator
def main():
    return run(sys.argv[1:])


def run(argv):
    options = Config.init(argv, parser)

    if options.formatter:
        Writer.set(options.formatter(options))
    else:
        Writer.set(GraphWriter(options))

    return DatabaseGrapher.graph(options)

if __name__ == "__main__":
    main()
