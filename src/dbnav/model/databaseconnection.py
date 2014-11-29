#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import reflection

from dbnav.logger import logduration, LogWith
from dbnav.querybuilder import QueryBuilder, SimplifyMapper
from dbnav.comment import create_comment
from dbnav.utils import tostring
from dbnav.model import DEFAULT_LIMIT
from dbnav.model.column import create_column
from dbnav.model.baseitem import BaseItem
from dbnav.model.foreignkey import ForeignKey
from dbnav.model.database import Database
from dbnav.model.row import Row
from dbnav.model.table import Table
from dbnav.model.tablecomment import TableComment, COMMENT_TITLE
from dbnav.model.value import Value
from dbnav.model.value import KIND_VALUE, KIND_FOREIGN_KEY, KIND_FOREIGN_VALUE

logger = logging.getLogger(__name__)

OPTION_URI_SINGLE_ROW_FORMAT = u'%s%s/?%s'
OPTION_URI_MULTIPLE_ROWS_FORMAT = u'%s%s?%s'


@LogWith(logger)
def foreign_key_or_column(table, column):
    fk = table.foreign_key(column)
    if fk:
        return fk
    return table.column(column)


@LogWith(logger)
def val(row, column):
    return row[tostring(column)]


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


class DatabaseConnection(BaseItem):
    def __init__(self, **kwargs):
        self.dbms = kwargs.get('dbms', None)
        self.database = kwargs.get('database', None)
        self.uri = kwargs.get('uri', None)
        self._inspector = None
        self._meta = None
        self._tables = kwargs.get('tbls', None)
        self._comments = kwargs.get('comments', None)

    def title(self):
        return self.__repr__()

    def subtitle(self):
        return 'Generic Connection'

    def autocomplete(self):
        return self.__repr__()

    def icon(self):
        return 'images/connection.png'

    def uri(self, table):
        return u'%s%s' % (self.autocomplete(), table)

    def matches(self, options):
        return options.arg in self.title()

    def proceed(self, options):
        if options.show == 'connections':
            # print this connection
            return [self]

        try:
            self.connect(options.database)

            if options.show == 'databases':
                dbs = self.databases()
                if options.database:
                    dbs = filter(lambda db: options.database in db.name, dbs)

                return sorted(dbs, key=lambda db: db.name.lower())

            if options.show == 'tables':
                tables = map(lambda (k, t): t, self.tables().iteritems())
                if options.table:
                    tables = filter(
                        lambda t: t.name.startswith(options.table),
                        tables)

                return sorted(tables, key=lambda t: t.name.lower())

            tables = self.tables()
            if options.table not in tables:
                raise Exception(
                    "Could not find table '{0}' on {1} ({2})".format(
                        options.table, self, self.dbms))

            table = tables[options.table]
            if options.show == 'columns':
                logger.debug('columns, check filter=%s', options.filter)
                if not options.filter:
                    raise Exception("No filter given")
                if len(options.filter) > 0 and options.filter[-1].rhs is None:
                    return sorted(
                        table.columns(options.filter[-1].lhs),
                        key=lambda c: c.name.lower())
                else:
                    return sorted(
                        self.rows(
                            table,
                            options.filter,
                            limit=options.limit,
                            simplify=options.simplify),
                        key=lambda r: r[0])

            if options.show == 'values':
                return values(self, table, options)
        finally:
            self.close()

    def connect(self, database):
        pass

    @LogWith(logger)
    def connect_to(self, source):
        self.engine = create_engine(source)
        self.con = self.engine.connect()

    def meta(self):
        if self._meta is None:
            self._meta = MetaData()
            self._meta.reflect(bind=self.engine)

        return self._meta

    def inspector(self):
        if self._inspector is None:
            self._inspector = reflection.Inspector.from_engine(self.engine)

        return self._inspector

    def connected(self):
        return self.con

    def close(self):
        if self.con:
            self.con.close()
            self.con = None

    def cursor(self):
        return self.con

    def begin(self):
        return self.con.begin()

    @LogWith(logger, log_args=False, log_result=False)
    def execute(self, query, name='Unnamed'):
        logger.info('Query %s: %s', name, query)

        cur = self.cursor()
        if not cur:
            raise Exception('Database is not connected')
        start = time.time()
        result = cur.execute(query)
        logduration('Query %s' % name, start)

        return result

    @LogWith(logger, log_args=False, log_result=False)
    def queryall(self, query, name='Unnamed', mapper=None):
        logger.info('Query all %s: %s', name, query)

        start = time.time()
        result = query.all()
        logduration('Query all %s' % name, start)

        if mapper:
            for row in result:
                mapper.map(row)

        return result

    @LogWith(logger, log_args=False, log_result=False)
    def queryone(self, query, name='Unnamed', mapper=None):
        logger.info('Query one %s: %s', name, query)

        start = time.time()
        result = query.one()
        logduration('Query one %s' % name, start)

        if mapper:
            mapper.map(result)

        return result

    def rows(self, table, filter=None, limit=DEFAULT_LIMIT, simplify=None):
        return table.rows(self, filter, limit, simplify)

    def filter(self, options):
        return True

    def databases(self):
        return map(
            lambda name: Database(self, name),
            self.inspector().get_schema_names())

    @LogWith(logger)
    def init_tables(self, database):
        self._tables = dict(map(
            lambda table: (table, Table(
                database, self.entity(table), self.autocomplete())),
            self.meta().tables))
        logger.debug('Tables: %s' % self._tables)
        self.init_foreign_keys()

    @LogWith(logger)
    def tables(self):
        if not self._tables:
            self.init_tables(self.database)

        return self._tables

    def table(self, tablename):
        return self.tables().get(tablename, None)

    def entity(self, tablename):
        return self.meta().tables[tablename]

    def init_comments(self):
        self._comments = dict(map(
            lambda k: (k, TableComment('')),
            self.tables().keys()))
        comment = self.table('_comment')
        if comment:
            # Table _comments exists, query it
            for row in self.rows(comment, limit=-1, simplify=False):
                self._comments[row['table']] = TableComment(row['comment'])

    def comments(self):
        if not self._comments:
            self.init_comments()

        return self._comments

    def comment(self, tablename):
        return self.comments().get(tablename, None)

    def init_foreign_keys(self):
        for k, t in self.meta().tables.iteritems():
            for _fk in t.foreign_keys:
                a = create_column(
                    self._tables[_fk.parent.table.name],
                    str(_fk.parent.key),
                    _fk.parent)
                b = create_column(
                    self._tables[_fk.column.table.name],
                    str(_fk.column.key),
                    _fk.column)
                fk = ForeignKey(a, b)
                self._tables[a.table.name].fks[a.name] = fk
                self._tables[b.table.name].fks[str(a)] = fk

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __getstate__(self):
        state = dict(self.__dict__)
        if 'con' in state:
            del state['con']
        return state
