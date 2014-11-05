#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

from collections import deque

from dbnav import decorator
from dbnav.config import Config
from dbnav.sources import Source
from dbnav.logger import logger
from dbnav.utils import prefixes, remove_prefix
from dbnav.node import ColumnNode, ForeignKeyNode, NameNode, TableNode
from dbnav.writer import Writer

from .args import parser
from .writer import GraphWriter, GraphvizWriter


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
                table.init_columns(table.connection)

                logger.debug(
                    'consume table=%s, include=%s, exclude=%s, consumed=%s, '
                    'indent=%d',
                    table, include, exclude, consumed, indent)

                for col in filter(
                        lambda col: col.name not in exclude, table.cols):
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
                    def f(key, fk):
                        return (
                            fk.b.table.name == table.name
                            and fk.a.table.name not in exclude)
                    for key, fk in filter(f, table.fks.iteritems()):
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
    def graph(options):
        """The main method that splits the arguments and starts the magic"""

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.driver)
            if connection.matches(opts) and opts.show in [
                    'tables', 'columns', 'values']:
                try:
                    connection.connect(opts.database)
                    tables = connection.tables()
                    if opts.table not in tables:
                        raise Exception(
                            "Could not find table '{0}'".format(opts.table))
                    table = tables[opts.table]
                    nodes = []
                    indent = 0
                    if opts.include_driver:
                        nodes.append(
                            NameNode(connection.driver, indent=indent))
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

        raise Exception('Specify the complete URI to a table')


def main():
    run(sys.argv)


@decorator
def run(argv):
    options = Config.init(argv, parser)

    if options.formatter:
        Writer.set(options.formatter())
    else:
        Writer.set(GraphWriter())

    return DatabaseGrapher.graph(options)

if __name__ == "__main__":
    main()
