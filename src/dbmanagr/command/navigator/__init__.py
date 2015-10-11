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

from dbmanagr import KIND_VALUE, KIND_FOREIGN_KEY, KIND_FOREIGN_VALUE
from dbmanagr import OPTION_URI_SINGLE_ROW_FORMAT
from dbmanagr import OPTION_URI_MULTIPLE_ROWS_FORMAT
from dbmanagr.wrapper import Wrapper
from dbmanagr.utils import tostring, foreign_key_or_column, find_connection
from dbmanagr.logger import LogWith
from dbmanagr.querybuilder import QueryBuilder, SimplifyMapper
from dbmanagr.exception import UnknownTableException
from dbmanagr.comment import create_comment
from dbmanagr.config import Config
from dbmanagr.writer import Writer
from dbmanagr.sources.source import Source
from dbmanagr.model.value import Value
from dbmanagr.model.row import Row
from dbmanagr.model.tablecomment import COMMENT_TITLE

from .dto import to_dto
from .args import parser
from .writer import SimplifiedWriter

logger = logging.getLogger(__name__)

IMAGE_CONNECTION = 'images/connection.png'
IMAGE_DATABASE = 'images/database.png'
IMAGE_TABLE = 'images/table.png'


def forward_references(row, table, keys, aliases):
    foreign_keys = table.foreign_keys()
    alias = aliases.get(table.name, table.name)

    refs = []
    for key in keys:
        k = key.replace('{0}_'.format(alias), '', 1)
        if key in foreign_keys:
            # Key is a foreign key column
            fk = foreign_keys[key]
            autocomplete = fk.b.table.autocomplete_(
                fk.b.name, row[tostring(key)])
        elif table.column(k).primary_key:
            # Key is a simple column, but primary key
            autocomplete = table.autocomplete_(
                k, row[tostring(key)], OPTION_URI_SINGLE_ROW_FORMAT)
        else:
            # Key is a simple column
            autocomplete = table.autocomplete_(
                k, row[tostring(key)], OPTION_URI_MULTIPLE_ROWS_FORMAT)
        f = foreign_key_or_column(table, k)
        kind = KIND_VALUE
        if f.__class__.__name__ == 'ForeignKey':
            kind = KIND_FOREIGN_KEY
        refs.append(Value(
            row[tostring(key)],
            str(f),
            autocomplete,
            True,
            kind))

    return refs


def back_references(row, table, aliases):
    foreign_keys = table.foreign_keys()

    refs = []
    for key in sorted(
            foreign_keys,
            key=lambda k: foreign_keys[k].a.table.name):
        fk = foreign_keys[key]
        if fk.b.table.name == table.name:
            autocomplete = fk.a.table.autocomplete_(
                fk.a.name, row['{0}_{1}'.format(
                    aliases.get(fk.b.table.name, fk.b.table.name), fk.b.name)],
                OPTION_URI_MULTIPLE_ROWS_FORMAT)
            logger.debug(
                'table.name=%s, fk=%s, autocomplete=%s',
                table.name, fk, autocomplete)
            refs.append(
                Value(
                    fk.a,
                    str(foreign_key_or_column(fk.a.table, fk.a.name)),
                    autocomplete,
                    False,
                    KIND_FOREIGN_VALUE))

    return refs


@LogWith(logger)
def create_databases(connection, options):
    databases = connection.databases()
    if options.database:
        databases = filter(lambda db: options.database in db.name, databases)

    return sorted(databases, key=lambda db: db.name.lower())


@LogWith(logger)
def create_values(connection, table, filter_):
    """Creates row values according to the given filter"""

    builder = QueryBuilder(
        connection,
        table,
        filter_=filter_.filter,
        limit=1,
        simplify=filter_.simplify)

    mapper = None
    keys = None
    if filter_.simplify:
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
        mapper)

    row = Row(table, result)

    logger.debug('Keys: %s', keys)
    if keys is None:
        keys = sorted(
            row.row.keys(),
            key=lambda key: '' if key == COMMENT_TITLE else tostring(key))
    logger.debug('Keys: %s', keys)

    values = forward_references(row, table, keys, builder.aliases)
    values += back_references(row, table, builder.aliases)

    return values


@LogWith(logger)
def create_tables(connection, options):
    tables = map(lambda (k, t): t, connection.tables().iteritems())
    if options.table:
        tables = filter(
            lambda t: t.name.startswith(options.table),
            tables)

    return sorted(tables, key=lambda t: t.name.lower())


def filter_complete(f):
    if not f:
        raise Exception("No filter given")
    return len(f) > 0 and f.last().rhs is not None


@LogWith(logger)
def create_rows(connection, table, options):
    return sorted(
        connection.rows(
            table,
            options.filter,
            limit=options.limit,
            simplify=options.simplify),
        key=lambda r: r[0])


@LogWith(logger)
def create_columns(table, options):
    return sorted(
        table.columns(options.filter.last().lhs),
        key=lambda c: c.name.lower())


def create(connection, options):
    if options.show == 'connections':
        # print this connection
        return [connection]

    try:
        connection.connect(options.database)

        if options.show == 'databases':
            return create_databases(connection, options)

        if options.show == 'tables':
            return create_tables(connection, options)

        tables = connection.tables()
        if options.table not in tables:
            raise UnknownTableException(options.table, tables.keys())

        table = tables[options.table]
        if options.show == 'columns':
            if filter_complete(options.filter):
                return create_rows(connection, table, options)
            return create_columns(table, options)

        if options.show == 'values':
            return create_values(connection, table, options)
    finally:
        connection.close()


class DatabaseNavigator(Wrapper):
    """The main class"""
    def __init__(self, options):
        Wrapper.__init__(self, options)

        if options.formatter:
            Writer.set(options.formatter())
        else:
            Writer.set(SimplifiedWriter())

    @LogWith(logger, log_result=False)
    def execute(self):
        """The main method that splits the arguments and starts the magic"""
        options = self.options

        return to_dto(self.build(options))

    def build(self, options):
        cons = Source.connections()

        # search exact match of connection
        connection, opts = find_connection(
            cons,
            options,
            lambda con, opts: (
                opts.show != 'connections' and con.matches(opts)))

        if connection is not None:
            return create(connection, opts)

        # print all connections
        return sorted(
            [c for c in cons if c.filter_(options)],
            key=lambda c: c.title().lower())


def execute(args):
    """
    Directly calls the execute method and avoids using the wrapper
    """
    return DatabaseNavigator(Config.init(args, parser)).execute()


def run(args):
    return DatabaseNavigator(Config.init(args, parser)).run()


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    return DatabaseNavigator(Config.init(args, parser)).write()
