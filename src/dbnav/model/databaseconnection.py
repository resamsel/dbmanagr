#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from sqlalchemy import *
from sqlalchemy.engine import reflection

from ..logger import *
from ..querybuilder import QueryBuilder, QueryFilter
from .column import *
from .baseitem import BaseItem

logger = logging.getLogger(__name__)

def values(connection, table, filter):
    """Creates row values according to the given filter"""
    
    logger.debug('values(connection=%s, table=%s, filter=%s)', connection, table, filter)

    foreign_keys = table.fks
    query = QueryBuilder(connection, table, filter=QueryFilter(filter.column, filter.operator, filter.filter), order=[], limit=1).build()
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
            return '%s (%s)' % (row.row[colname], row.row[column])
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

class Row:
    columns = {'id': 1, 'title': 'Title', 'subtitle': 'Subtitle', 'column_name': 'column', 0: '0', 1: '1', 'column': 'col'}
    def __init__(self, *args):
        if len(args) > 0:
            self.columns = args[0]
            if 'id' not in self.columns:
                self.columns['id'] = 0
        else:
            self.columns = Row.columns.copy()
    def __getitem__(self, i):
        logger.debug('Row.__getitem__(%s: %s)', str(i), type(i))
        if i == None:
            return None
        return self.columns[i]
    def __contains__(self, item):
        return item in self.columns

class Cursor:
    def execute(self, query):
        pass
    def fetchone(self):
        return Row()
    def fetchall(self):
        return [Row()]

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
        return '%s%s' % (self.autocomplete(), table)

    def matches(self, options):
        return options.arg in self.title()

    def proceed(self, options, auto_close=True):
        if options.show == 'connections':
            # print this connection
            return [self]

        try:
            self.connect(options.database)

            if options.show == 'databases':
                dbs = self.databases()
                if options.database:
                    dbs = [db for db in dbs if options.database in db.name]

                return sorted(dbs, key=lambda db: db.name.lower())

            if options.show == 'tables':
                tables = [t for k, t in self.tables().iteritems()]
                if options.table:
                    tables = [t for t in tables if t.name.startswith(options.table)]

                return sorted(tables, key=lambda t: t.name.lower())

            table = self.tables()[options.table]
            if options.show == 'columns':
                if options.filter == None:
                    return sorted(table.columns(self, options.column), key=lambda c: c.name.lower())
                else:
                    return sorted(table.rows(QueryFilter(options.column, options.operator, options.filter), artificial_projection=options.artificial_projection), key=lambda r: r[0])
            
            if options.show == 'values':
                return values(self, table, options)
        finally:
            if auto_close:
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
        pks = [pk for pk in self.inspector.get_pk_constraint(table.name)['constrained_columns']]
        
        logger.debug('Columns for %s: %s', table, cols)
        return [Column(table, col['name'], [col['name']] == pks, col['type']) for col in cols]

    def restriction(self, alias, column, operator, value):
        return "{0}.{1} {2} {3}".format(alias, column.name, operator, self.format_value(column, value))

    def format_value(self, column, value):
        return "'{0}'".format(value)

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
