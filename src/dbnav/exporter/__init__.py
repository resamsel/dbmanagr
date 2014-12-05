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
import re
import logging

from collections import OrderedDict

from dbnav import Wrapper
from dbnav.logger import LogWith
from dbnav.config import Config
from dbnav.sources import Source
from dbnav.utils import remove_prefix
from dbnav.queryfilter import QueryFilter
from dbnav.formatter import Formatter
from dbnav.writer import Writer
from dbnav.exception import UnknownColumnException, UnknownTableException

from .args import parser, SqlInsertWriter

logger = logging.getLogger(__name__)


class RowItem():
    def __init__(self, row, exclude):
        self.row = row
        self.exclude = exclude

    def __hash__(self):
        return hash(self.row.autocomplete())

    def __eq__(self, o):
        return hash(self.row.autocomplete()) == hash(o.row.autocomplete())

    def format(self):
        Formatter.formatter.format_row(self.row)


def fk_by_a_table_name(fks):
    return dict(map(lambda (k, v): (v.a.table.name, v), fks.iteritems()))


@LogWith(logger)
def create_items(connection, items, include, exclude):
    results_pre = []
    results_post = []
    includes = {}
    for item in items:
        for i in include:
            c = re.sub('([^\\.]*)\\..*', '\\1', i)
            fk = None
            for key, val in item.table.fks.iteritems():
                if val.a.table.name == c:
                    fk = val
                    break
            col = item.table.column(c)
            if not col and not fk:
                raise UnknownColumnException(item.table, i)
            if fk:
                # fk.a.table.connection = item.table.connection
                if fk not in includes:
                    includes[fk] = []
                includes[fk].append(item[fk.b.name])
            if col and col.name in item.table.fks:
                fk = item.table.fks[col.name]
                # fk.b.table.connection = item.table.connection
                if fk not in includes:
                    includes[fk] = []
                includes[fk].append(item[fk.a.name])
    if exclude:
        for item in items:
            for x in exclude:
                c = re.sub('([^\\.]*)\\..*', '\\1', x)
                fks = fk_by_a_table_name(item.table.fks)
                fk = None
                if c in fks:
                    fk = fks[c]
                col = item.table.column(c)
                if not col and not fk:
                    raise UnknownColumnException(
                        item.table, x,
                        fks.keys() + map(
                            lambda c: c.name, item.table.columns()))
            # only check first item, as we expect all items are from the same
            # table
            break
    for fk in includes.keys():
        if fk.a.table.name == item.table.name:
            # forward references, must be in pre
            results_pre += create_items(
                connection,
                connection.rows(
                    fk.b.table,
                    QueryFilter(fk.b.name, 'in', includes[fk]),
                    limit=-1,
                    simplify=False),
                remove_prefix(fk.a.name, include),
                remove_prefix(fk.a.name, exclude))
        else:
            # backward reference, must be in post
            results_post += create_items(
                connection,
                connection.rows(
                    fk.a.table,
                    QueryFilter(fk.a.name, 'in', includes[fk]),
                    limit=-1,
                    simplify=False),
                remove_prefix(fk.a.table.name, include),
                remove_prefix(fk.a.table.name, exclude))

    return results_pre + map(
        lambda i: RowItem(i, exclude), items) + results_post


def prefix(s):
    return re.sub('([^\\.]*)\\..*', '\\1', s)


class DatabaseExporter(Wrapper):
    """The main class"""
    def __init__(self, options):
        self.options = options

        if options.formatter:
            Writer.set(options.formatter(options))
        else:
            Writer.set(SqlInsertWriter(options))

    def execute(self):
        """The main method that splits the arguments and starts the magic"""
        options = self.options

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.dbms)
            if ((opts.show == 'values'
                    or opts.show == 'columns' and opts.filter is not None)
                    and connection.matches(opts)):
                try:
                    connection.connect(opts.database)
                    tables = connection.tables()
                    if opts.table not in tables:
                        raise UnknownTableException(opts.table, tables.keys())
                    table = tables[opts.table]
                    items = create_items(
                        connection,
                        connection.rows(
                            table,
                            opts.filter,
                            opts.limit,
                            simplify=False),
                        opts.include,
                        opts.exclude)
                    # remove duplicates
                    return list(OrderedDict.fromkeys(items))
                finally:
                    connection.close()

        raise Exception('Specify the complete URI to a table')


def run(args):
    exporter = DatabaseExporter(Config.init(args, parser))
    return exporter.run()


def main():
    exporter = DatabaseExporter(Config.init(sys.argv[1:], parser))
    return exporter.write()
