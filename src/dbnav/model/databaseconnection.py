#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from sqlalchemy import *
from sqlalchemy.engine import reflection
from sqlalchemy.types import TIMESTAMP
import datetime

from ..logger import *
from ..querybuilder import QueryBuilder
from .column import *
from dbnav.item import VALID, INVALID
from .baseitem import BaseItem
from dbnav.model.row import Row
from dbnav.model.value import Value, KIND_VALUE, KIND_FOREIGN_KEY, KIND_FOREIGN_VALUE

logger = logging.getLogger(__name__)

OPTION_URI_TABLES_FORMAT = u'%s%s/'
OPTION_URI_ROW_FORMAT = u'%s%s/%s'

def tostring(key):
    if isinstance(key, unicode):
        return key.encode('ascii', errors='ignore')
    return key

def values(connection, table, filter):
    """Creates row values according to the given filter"""
    
    logger.debug('values(connection=%s, table=%s, filter=%s)', connection, table, filter)

    foreign_keys = table.fks
    query = QueryBuilder(connection,
                table,
                filter=filter.filter,
                order=[],
                limit=1,
                simplify=filter.simplify).build()
    result = connection.execute(query, 'Values')
        
    row = Row(connection, table, result.fetchone())

    logger.debug('Comment.display: %s', table.comment.display)
    if table.comment.display:
        keys = table.comment.display
    else:
        keys = sorted(row.row.keys(), key=lambda key: '' if key == COMMENT_TITLE else tostring(key))

    def fkey(column): return foreign_keys[column.name] if column.name in foreign_keys else column

    def val(row, column):
        colname = '%s_title' % column
        if colname in row.row:
            return u'%s (%s)' % (row.row[colname], row.row[column])
        return row.row[tostring(column)]

    values = []
    for key in keys:
        value = val(row, key)
        if key in table.fks:
            # if key is a foreign key column
            fk = table.fks[key]
            autocomplete = fk.b.table.autocomplete(fk.b.name, row.row[tostring(key)])
        else:
            autocomplete = table.autocomplete(key, row.row[tostring(key)], OPTION_URI_ROW_FORMAT)
        f = fkey(Column(table, key))
        kind = KIND_VALUE
        if f.__class__.__name__ == 'ForeignKey':
            kind = KIND_FOREIGN_KEY
        values.append(Value(value, f, autocomplete, VALID, kind))

    for key in sorted(foreign_keys, key=lambda k: foreign_keys[k].a.table.name):
        fk = foreign_keys[key]
        if fk.b.table.name == table.name:
            autocomplete = fk.a.table.autocomplete(fk.a.name, row.row[fk.b.name], OPTION_URI_ROW_FORMAT)
            logger.debug('table.name=%s, fk=%s, autocomplete=%s', table.name, fk, autocomplete)
            values.append(
                Value(fk.a,
                    fkey(Column(fk.a.table, fk.a.name)),
                    autocomplete,
                    INVALID,
                    KIND_FOREIGN_VALUE))

    return values

class DatabaseRow:
    columns = {'id': 1, 'title': 'Title', 'subtitle': 'Subtitle', 'column_name': 'column', 0: '0', 1: '1', 'column': 'col'}
    def __init__(self, *args):
        self.columns = DatabaseRow.columns.copy()
        if len(args) > 0:
            self.columns.update(args[0])
            if 'id' not in self.columns:
                self.columns['id'] = 0
    def __getitem__(self, i):
        logger.debug('DatabaseRow.__getitem__(%s: %s), columns=%s', str(i), type(i), self.columns)
        if i == None:
            return None
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
    def __init__(self, *args):
        self.database = None
        self.tbls = None
        self.driver = None

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
                raise Exception("Could not find table '{0}'".format(options.table))

            table = tables[options.table]
            if options.show == 'columns':
                logger.debug('columns, check filter=%s', options.filter)
                if len(options.filter) > 0 and options.filter[-1].rhs == None:
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
        self.engine = create_engine(source)
        self.con = self.engine.connect()
        self.inspector = reflection.Inspector.from_engine(self.engine)

    def connected(self):
        return self.con

    def close(self):
        if self.con:
            self.con.close()
            self.con = None

    def cursor(self):
        return self.con

    def execute(self, query, name='Unnamed'):
        logger.info('Query %s: %s', name, query)
        
        cur = self.cursor()
        if not cur:
            raise Exception('Database is not connected')
        start = time.time()
        result = cur.execute(query)
        logduration('Query %s' % name, start)
        
        return result

    def filter(self, options):
        return True

    def databases(self):
        return []

    def tables(self):
        if not self.tbls:
            self.tbls = {t.name.encode('ascii'): t for t in self.tablesof(self.database)}
            logger.debug('Table Map: %s' % self.tbls)
            self.put_foreign_keys()

        return self.tbls

    def tablesof(self, database):
        return {}

    def put_foreign_keys(self):
        pass

    def columns(self, table):
        """Returns a list of Column objects"""

        cols = self.inspector.get_columns(table.name)
        pks = self.inspector.get_pk_constraint(table.name)['constrained_columns']
        
        return map(
            lambda col: Column(
                table,
                col['name'],
                [col['name']] == pks,
                col['type'],
                col['nullable']),
            cols)

    def restriction(self, alias, column, operator, value):
        if column.table:
            return u"{0}.{1} {2} {3}".format(alias, column.name, operator, self.format_value(column, value))
        return u'{0} {1} {2}'.format(column.name, operator, self.format_value(column, value))

    def format_value(self, column, value):
        #print column.type, value, value == None
        if value == None:
            return 'null'
        if type(value) is list:
            return '({0})'.format(','.join([self.format_value(column, v) for v in value]))
        if type(value) in [datetime.datetime, datetime.date, datetime.time]:
            return "'%s'" % value
        if type(value) is buffer:
            return u"'[BLOB]'"
        if column is None:
            try:
                return '%d' % int(value)
            except ValueError:
                return u"'%s'" % value
        if isinstance(column.type, Boolean) and (type(value) is bool or value in ['true', 'false']):
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
