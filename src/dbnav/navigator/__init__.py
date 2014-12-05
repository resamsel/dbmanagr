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

import logging
import sys

from dbnav import Wrapper
from dbnav import KIND_VALUE, KIND_FOREIGN_KEY, KIND_FOREIGN_VALUE
from dbnav import OPTION_URI_SINGLE_ROW_FORMAT
from dbnav import OPTION_URI_MULTIPLE_ROWS_FORMAT
from dbnav.utils import tostring, foreign_key_or_column
from dbnav.logger import LogWith
from dbnav.querybuilder import QueryBuilder, SimplifyMapper
from dbnav.exception import UnknownTableException
from dbnav.comment import create_comment
from dbnav.config import Config
from dbnav.writer import Writer
from dbnav.sources import Source
from dbnav.model.value import Value
from dbnav.model.row import Row
from dbnav.model.tablecomment import COMMENT_TITLE
from .args import parser
from .writer import SimplifiedWriter

logger = logging.getLogger(__name__)

IMAGE_CONNECTION = 'images/connection.png'
IMAGE_DATABASE = 'images/database.png'
IMAGE_TABLE = 'images/table.png'


def forward_references(row, table, keys, aliases):
    foreign_keys = table.foreign_keys()
    alias = aliases[table.name]

    refs = []
    for key in keys:
        k = key.replace('{0}_'.format(alias), '', 1)
        if key in foreign_keys:
            # Key is a foreign key column
            fk = foreign_keys[key]
            autocomplete = fk.b.table.autocomplete(
                fk.b.name, row[tostring(key)])
        elif table.column(k).primary_key:
            # Key is a simple column, but primary key
            autocomplete = table.autocomplete(
                k, row[tostring(key)], OPTION_URI_SINGLE_ROW_FORMAT)
        else:
            # Key is a simple column
            autocomplete = table.autocomplete(
                k, row[tostring(key)], OPTION_URI_MULTIPLE_ROWS_FORMAT)
        f = foreign_key_or_column(table, k)
        kind = KIND_VALUE
        if f.__class__.__name__ == 'ForeignKey':
            kind = KIND_FOREIGN_KEY
        refs.append(Value(row[tostring(key)], f, autocomplete, True, kind))

    return refs


def back_references(row, table, aliases):
    foreign_keys = table.foreign_keys()

    refs = []
    for key in sorted(
            foreign_keys,
            key=lambda k: foreign_keys[k].a.table.name):
        fk = foreign_keys[key]
        if fk.b.table.name == table.name:
            autocomplete = fk.a.table.autocomplete(
                fk.a.name, row['{0}_{1}'.format(
                    aliases[fk.b.table.name], fk.b.name)],
                OPTION_URI_MULTIPLE_ROWS_FORMAT)
            logger.debug(
                'table.name=%s, fk=%s, autocomplete=%s',
                table.name, fk, autocomplete)
            refs.append(
                Value(
                    fk.a,
                    foreign_key_or_column(fk.a.table, fk.a.name),
                    autocomplete,
                    False,
                    KIND_FOREIGN_VALUE))

    return refs


@LogWith(logger)
def values(connection, table, filter):
    """Creates row values according to the given filter"""

    builder = QueryBuilder(
        connection,
        table,
        filter=filter.filter,
        limit=1,
        simplify=filter.simplify)

    mapper = None
    keys = None
    if filter.simplify:
        comment = create_comment(
            table,
            connection.comment(table.name),
            builder.counter,
            builder.aliases,
            None)

        keys = comment.display

        mapper = SimplifyMapper(
            table,
            comment=comment)

    result = connection.queryone(
        builder.build(),
        'Values',
        mapper)

    row = Row(table, result)

    if keys is None:
        keys = sorted(
            row.row.keys(),
            key=lambda key: '' if key == COMMENT_TITLE else tostring(key))

    values = forward_references(row, table, keys, builder.aliases)
    values += back_references(row, table, builder.aliases)

    return values


def proceed(connection, options):
    if options.show == 'connections':
        # print this connection
        return [connection]

    try:
        connection.connect(options.database)

        if options.show == 'databases':
            dbs = connection.databases()
            if options.database:
                dbs = filter(lambda db: options.database in db.name, dbs)

            return sorted(dbs, key=lambda db: db.name.lower())

        if options.show == 'tables':
            tables = map(lambda (k, t): t, connection.tables().iteritems())
            if options.table:
                tables = filter(
                    lambda t: t.name.startswith(options.table),
                    tables)

            return sorted(tables, key=lambda t: t.name.lower())

        tables = connection.tables()
        if options.table not in tables:
            raise UnknownTableException(options.table, tables.keys())

        table = tables[options.table]
        if options.show == 'columns':
            logger.debug('columns, check filter=%s', options.filter)
            if not options.filter:
                raise Exception("No filter given")
            if (len(options.filter) > 0
                    and options.filter.last().rhs is None):
                return sorted(
                    table.columns(options.filter.last().lhs),
                    key=lambda c: c.name.lower())
            else:
                return sorted(
                    connection.rows(
                        table,
                        options.filter,
                        limit=options.limit,
                        simplify=options.simplify),
                    key=lambda r: r[0])

        if options.show == 'values':
            return values(connection, table, options)
    finally:
        connection.close()


class DatabaseNavigator(Wrapper):
    """The main class"""
    def __init__(self, options):
        self.options = options

        if options.formatter:
            Writer.set(options.formatter())
        else:
            Writer.set(SimplifiedWriter())

    @LogWith(logger, log_result=False)
    def execute(self):
        """The main method that splits the arguments and starts the magic"""
        options = self.options

        cons = Source.connections()

        # search exact match of connection
        for connection in cons:
            opts = options.get(connection.dbms)
            if opts.show != 'connections' and connection.matches(opts):
                return proceed(connection, opts)

        # print all connections
        return sorted(
            [c for c in cons if c.filter(options)],
            key=lambda c: c.title().lower())


def run(args):
    navigator = DatabaseNavigator(Config.init(args, parser))
    return navigator.run()


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    navigator = DatabaseNavigator(Config.init(args, parser))
    return navigator.write()
