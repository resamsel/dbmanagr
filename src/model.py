#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import psycopg2
import psycopg2.extras
import json

from const import *
from querybuilder import QueryBuilder

DEFAULT_LIMIT = 50
ID_FORMAT = "{0}.id"

class Database:
    """The database used with the given connection"""

    def __init__(self, connection, name):
        self.connection = connection
        self.name = name

    def __repr__(self):
        return "%s@%s/%s" % (self.connection.user, self.connection.host, self.name)

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        return OPTION_URI_DATABASE_FORMAT % (self.__repr__())

class TableComment:
    """The comment on the given table that allows to display much more accurate information"""

    def __init__(self, table, json_string):
        self.d = {COMMENT_TITLE: ID_FORMAT, COMMENT_ORDER_BY: [], COMMENT_SEARCH: [], COMMENT_DISPLAY: []}
        self.d[COMMENT_SUBTITLE] = "'Id: ' || %s" % ID_FORMAT
        self.d[COMMENT_ID] = ID_FORMAT

        if json_string:
            try:
                self.d = dict(self.d.items() + json.loads(json_string).items())
            except TypeError, e:
                pass

        self.id = self.d[COMMENT_ID]
        if self.d[COMMENT_TITLE] == ID_FORMAT and self.id != ID_FORMAT:
            self.d[COMMENT_TITLE] = '{0}.%s' % self.id
#        logging.debug('Comment on %s: %s', table, self.d)
        self.title = self.d[COMMENT_TITLE]
        self.subtitle = self.d[COMMENT_SUBTITLE]
        self.search = self.d[COMMENT_SEARCH]
        self.display = self.d[COMMENT_DISPLAY]
        self.order = self.d[COMMENT_ORDER_BY]

    def __repr__(self):
        return self.d.__repr__()

class Table:
    def __init__(self, connection, database, name, comment):
        self.connection = connection
        self.database = database
        self.name = name
        self.comment = TableComment(self, comment)
        self.cols = None
        self.fks = {}

    def __repr__(self):
        return self.name

    def uri(self):
        """Creates the URI for this table"""

        return '%s@%s/%s' % (self.connection.user, self.connection.host, self.database)

    def autocomplete(self, column, value):
        """Retrieves the autocomplete string for the given column and value"""

        tablename = self.name
        fks = self.fks
        if column in fks:
            fk = fks[column]
            tablename = fk.b.table.name

        return OPTION_URI_VALUE_FORMAT % (self.uri(), tablename, value)

    def rows(self, filter):
        """Retrieves rows from the table with the given filter applied"""

        query = QueryBuilder(self, filter=filter, order=self.comment.order, limit=DEFAULT_LIMIT).build()

        logging.debug('Query rows: %s' % query)
        cur = self.connection.cursor()
        cur.execute(query)

        def t(row): return Row(self.connection, self, row)

        return map(t, cur.fetchall())
    
    def columns(self):
        """Retrieves the columns of the table"""

        if not self.cols:
            logging.debug('Retrieve columns')
            query = COLUMNS_QUERY.format(self.name)
            logging.debug('Query columns: %s' % query)
            cur = self.connection.cursor()
            cur.execute(query)
            self.cols = []
            for row in cur.fetchall():
                self.cols.append(row['column_name'])

        return self.cols

class Row:
    """A table row from the database"""

    def __init__(self, connection, table, row):
        self.connection = connection
        self.table = table
        self.row = row

    def __getitem__(self, i):
        return self.row[i]

    def values(self):
        return self.row

class Column:
    """A table column"""

    def __init__(self, table, name):
        self.table = table
        self.name = name

    def __repr__(self):
        return '%s.%s' % (self.table.name, self.name)

class ForeignKey:
    """A foreign key connection between the originating column a and the foreign column b"""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return '%s -> %s' % (self.a, self.b)

class DatabaseConnection:
    """A database connection"""

    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.con = None
        self.dbs = None
        self.tbls = None

    def __repr__(self):
        return '%s@%s/%s' % (self.user, self.host, self.database if self.database != '*' else '')

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        if self.database and self.database != '*':
            return '%s@%s/%s/' % (self.user, self.host, self.database)

        return '%s@%s/' % (self.user, self.host)

    def matches(self, s):
        return s.startswith("%s@%s" % (self.user, self.host))

    def connect(self, database):
        logging.debug('Connecting to database %s' % database)
        
        if database:
            try:
                self.con = psycopg2.connect(host=self.host, database=database, user=self.user, password=self.password)
            except psycopg2.DatabaseError, e:
                self.con = psycopg2.connect(host=self.host, user=self.user, password=self.password)
        else:
            self.con = psycopg2.connect(host=self.host, user=self.user, password=self.password)
        self.table_map = {t.name: t for t in self.tables(database)}
        self.put_foreign_keys()

    def cursor(self):
        return self.con.cursor(cursor_factory=psycopg2.extras.DictCursor)

    def databases(self):
        if not self.dbs:
            query = DATABASES_QUERY
            logging.debug('Query databases: %s' % query)

            cur = self.cursor()
            cur.execute(query)
    
            def d(row): return Database(self, row[0])
    
            self.dbs = map(d, cur.fetchall())
        
        return self.dbs

    def tables(self, database):
        if not self.tbls:
            query = TABLES_QUERY
            logging.debug('Query tables: %s' % query)
    
            cur = self.cursor()
            cur.execute(query)
    
            def t(row): return Table(self, database, row[0], row[1])
    
            self.tbls = map(t, cur.fetchall())

        return self.tbls

    def put_foreign_keys(self):
        """Retrieves the foreign keys of the table"""

        logging.debug('Retrieve foreign keys')
        query = FOREIGN_KEY_QUERY
        logging.debug('Query foreign keys: %s' % query)
        cur = self.cursor()
        cur.execute(query)
        for row in cur.fetchall():
            a = Column(self.table_map[row['table_name']], row['column_name'])
            b = Column(self.table_map[row['foreign_table_name']], row['foreign_column_name'])
            fk = ForeignKey(a, b)
            self.table_map[a.table.name].fks[a.name] = fk
            self.table_map[b.table.name].fks[a.name] = fk
