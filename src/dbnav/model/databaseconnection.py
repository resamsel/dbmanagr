#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import math
import datetime

from sqlalchemy import create_engine, MetaData, Boolean, Float, Integer
from sqlalchemy.engine import reflection
from sqlalchemy.types import TIMESTAMP

from dbnav.logger import logduration, log_with
from dbnav.querybuilder import QueryBuilder, SimplifyMapper
from dbnav.comment import Comment
from dbnav.utils import tostring, dictsplus, dictminus
from dbnav.model.column import Column
from dbnav.model.baseitem import BaseItem
from dbnav.model.foreignkey import ForeignKey
from dbnav.model.database import Database
from dbnav.model.row import Row
from dbnav.model.table import Table
from dbnav.model.tablecomment import TableComment, COMMENT_TITLE
from dbnav.model.value import Value
from dbnav.model.value import KIND_VALUE, KIND_FOREIGN_KEY, KIND_FOREIGN_VALUE
from dbnav.model.exception import UnknownColumnException

logger = logging.getLogger(__name__)

OPTION_URI_SINGLE_ROW_FORMAT = u'%s%s/?%s'
OPTION_URI_MULTIPLE_ROWS_FORMAT = u'%s%s?%s'


@log_with(logger)
def values(connection, table, filter):
    """Creates row values according to the given filter"""

    foreign_keys = table.fks
    builder = QueryBuilder(
        connection,
        table,
        filter=filter.filter,
        limit=1,
        simplify=filter.simplify)

    comment = connection.comment(table.name)

    result = connection.queryone(
        builder.build(),
        'Values',
        SimplifyMapper(
            table,
            comment=Comment(
                table,
                comment,
                builder.counter,
                builder.aliases,
                None)))

    row = Row(connection, table, result)

    logger.debug('Comment.display: %s', comment.display)
    if comment.display:
        keys = comment.display
    else:
        keys = sorted(
            row.row.keys(),
            key=lambda key: '' if key == COMMENT_TITLE else tostring(key))

    def fkey(column):
        if column.name in foreign_keys:
            return foreign_keys[column.name]
        return column

    def val(row, column):
        colname = '%s_title' % column
        if colname in row.row:
            return u'%s (%s)' % (row[colname], row[column])
        return row[tostring(column)]

    values = []
    for key in keys:
        value = val(row, key)
        if key in table.fks:
            # Key is a foreign key column
            fk = table.fks[key]
            autocomplete = fk.b.table.autocomplete(
                fk.b.name, row[tostring(key)])
        elif table.column(key).primary_key:
            # Key is a simple column, but primary key
            autocomplete = table.autocomplete(
                key, row[tostring(key)], OPTION_URI_SINGLE_ROW_FORMAT)
        else:
            # Key is a simple column
            autocomplete = table.autocomplete(
                key, row[tostring(key)], OPTION_URI_MULTIPLE_ROWS_FORMAT)
        f = fkey(Column(table, key))
        kind = KIND_VALUE
        if f.__class__.__name__ == 'ForeignKey':
            kind = KIND_FOREIGN_KEY
        values.append(Value(value, f, autocomplete, True, kind))

    for key in sorted(
            foreign_keys, key=lambda k: foreign_keys[k].a.table.name):
        fk = foreign_keys[key]
        if fk.b.table.name == table.name:
            autocomplete = fk.a.table.autocomplete(
                fk.a.name, row[fk.b.name], OPTION_URI_MULTIPLE_ROWS_FORMAT)
            logger.debug(
                'table.name=%s, fk=%s, autocomplete=%s',
                table.name, fk, autocomplete)
            values.append(
                Value(
                    fk.a,
                    fkey(Column(fk.a.table, fk.a.name)),
                    autocomplete,
                    False,
                    KIND_FOREIGN_VALUE))

    return values


class DatabaseRow:
    columns = {
        'id': 1,
        'title': 'Title',
        'subtitle': 'Subtitle',
        'column_name': 'column',
        0: '0',
        1: '1',
        'column': 'col'
    }

    def __init__(self, *args):
        self.columns = DatabaseRow.columns.copy()
        if len(args) > 0:
            self.columns.update(args[0])
            if 'id' not in self.columns:
                self.columns['id'] = 0

    @log_with(logger)
    def __getitem__(self, i):
        if i is None:
            return None
        if type(i) is str and i not in self.columns:
            raise UnknownColumnException(None, i, map(
                lambda (k, v): k,
                filter(
                    lambda (k, v): type(k) is str,
                    self.columns.iteritems())))
        return self.columns[i]

    def __contains__(self, item):
        return item in self.columns


class Cursor:
    def execute(self, query):
        pass

    def fetchone(self):
        return DatabaseRow()

    def fetchall(self):
        return [DatabaseRow()]


class DatabaseConnection(BaseItem):
    def __init__(self, **kwargs):
        self.database = kwargs.get('database', None)
        self.driver = kwargs.get('driver', None)
        self._tables = kwargs.get('tbls', None)
        self._comments = kwargs.get('comments', None)

    def title(self):
        return 'Title'

    def subtitle(self):
        return 'Subtitle'

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        return 'Autocomplete'

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
                        options.table, self, self.driver))

            table = tables[options.table]
            if options.show == 'columns':
                logger.debug('columns, check filter=%s', options.filter)
                if not options.filter:
                    raise Exception("No filter given")
                if len(options.filter) > 0 and options.filter[-1].rhs is None:
                    return sorted(
                        table.columns(self, options.filter[-1].lhs),
                        key=lambda c: c.name.lower())
                else:
                    return sorted(
                        table.rows(
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

    def connect_to(self, source):
        logger.debug('Connecting to %s', source)
        self.engine = create_engine(source)
        self.con = self.engine.connect()
        self.inspector = reflection.Inspector.from_engine(self.engine)
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)

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

    def execute(self, query, name='Unnamed'):
        logger.info('Query %s: %s', name, query)

        cur = self.cursor()
        if not cur:
            raise Exception('Database is not connected')
        start = time.time()
        result = cur.execute(query)
        logduration('Query %s' % name, start)

        return result

    def queryall(self, query, name='Unnamed', mapper=None):
        logger.info('Query all %s: %s', name, query)

        start = time.time()
        result = query.all()
        logduration('Query all %s' % name, start)

        if mapper:
            for row in result:
                mapper.map(row)

        return result

    def queryone(self, query, name='Unnamed', mapper=None):
        logger.info('Query one %s: %s', name, query)

        start = time.time()
        result = query.one()
        logduration('Query one %s' % name, start)

        if mapper:
            mapper.map(result)

        return result

    def filter(self, options):
        return True

    def databases(self):
        return map(
            lambda name: Database(self, name),
            self.inspector.get_schema_names())

    def init_tables(self, database):
        self._tables = dict(map(
            lambda name: (name, Table(self, database, name)),
            self.inspector.get_table_names()))
        logger.debug('Tables: %s' % self._tables)
        self.init_foreign_keys()

    def tables(self):
        if not self._tables:
            self.init_tables(self.database)

        return self._tables

    def table(self, tablename):
        return self.tables().get(tablename, None)

    def init_comments(self):
        self._comments = dict(map(
            lambda k: (k, TableComment('')),
            self.tables().keys()))
        comment = self.table('_comment')
        if comment:
            # Table _comments exists, query it
            for row in comment.rows():
                self._comments[row['table']] = TableComment(row['comment'])

    def comments(self):
        if not self._comments:
            self.init_comments()

        return self._comments

    def comment(self, tablename):
        return self.comments().get(tablename, None)

    def init_foreign_keys(self):
        fks = reduce(
            lambda x, y: x + y,
            map(
                lambda (k, v): dictsplus(
                    self.inspector.get_foreign_keys(k), 'name', k),
                self._tables.iteritems()),
            [])

        for _fk in fks:
            a = Column(
                self._tables[_fk['name']],
                _fk['constrained_columns'][0])
            b = Column(
                self._tables[_fk['referred_table']],
                _fk['referred_columns'][0])
            fk = ForeignKey(a, b)
            self._tables[a.table.name].fks[a.name] = fk
            self._tables[b.table.name].fks[str(a)] = fk

    def columns(self, table):
        """Returns a list of Column objects"""

        cols = self.inspector.get_columns(table.name)
        pks = self.inspector.get_pk_constraint(
            table.name)['constrained_columns']

        return map(
            lambda col: Column(
                table,
                primary_key=[col['name']] == pks,
                **dictminus(col, 'primary_key')),
            cols)

    def restriction(
            self, alias, column, operator, value, map_null_operator=True):
        if not column:
            raise Exception('Column is None!')
        if column.table and alias is not None:
            return u"{0}.{1} {2} {3}".format(
                alias,
                self.escape_keyword(column.name),
                operator,
                self.format_value(column, value))
        if operator in ['=', '!='] and (value == 'null' or value is None):
            if map_null_operator:
                operator = {
                    '=': 'is',
                    '!=': 'is not'
                }.get(operator)
            value = None
        return u'{0} {1} {2}'.format(
            self.escape_keyword(column.name),
            operator,
            self.format_value(column, value))

    def format_value(self, column, value):
        if value is None or (type(value) is float and math.isnan(value)):
            return 'null'
        if type(value) is list:
            return '({0})'.format(
                ','.join([self.format_value(column, v) for v in value]))
        if type(value) in [datetime.datetime, datetime.date, datetime.time]:
            return "'%s'" % value
        if type(value) is buffer:
            return u"'[BLOB]'"
        if column is None:
            try:
                return '%d' % int(value)
            except ValueError:
                return u"'%s'" % value
        if (isinstance(column.type, Boolean)
                and (type(value) is bool or value in ['true', 'false'])):
            return '%s' % str(value).lower()
        if isinstance(column.type, Float):
            try:
                return '%f' % float(value)
            except ValueError:
                pass
        if isinstance(column.type, Integer):
            try:
                return '%d' % int(value)
            except ValueError:
                pass
        if isinstance(column.type, TIMESTAMP):
            try:
                return '%d' % int(value)
            except ValueError:
                pass
        return u"'%s'" % value.replace('%', '%%').replace("'", "''")

    def escape_keyword(self, keyword):
        if keyword in ['user', 'table', 'column']:
            return '"%s"' % keyword
        return keyword

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __getstate__(self):
        state = dict(self.__dict__)
        logger.debug('State: %s' % state)
        if 'con' in state:
            del state['con']
        return state
