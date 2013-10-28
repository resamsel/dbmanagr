#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import logging
#import psycopg2
#import psycopg2.extras
import time

from sqlalchemy import *
from sqlalchemy.engine import reflection
from sqlalchemy.exc import OperationalError
from os.path import expanduser

from ..logger import logduration
from ..model.databaseconnection import *
from ..model.database import *
from ..model.table import *
from ..model.column import *
from ..model.foreignkey import *

CACHE_TIME = 2*60
DATABASES_QUERY = """
select
        datname as database_name
    from
        pg_database
    where
        datistemplate = false
    order by datname
"""
FOREIGN_KEY_QUERY = """
select
        tc.table_name,
        kcu.column_name,
        ccu.table_name foreign_table_name,
        ccu.column_name foreign_column_name
    from
        information_schema.table_constraints tc
        join information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
        join information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
    where
        constraint_type = 'FOREIGN KEY'
"""
TABLES_QUERY = """
select
        t.table_name as tbl, obj_description(c.oid) as comment
    from
        information_schema.tables t,
        pg_class c
    where
        table_schema = 'public'
        and t.table_name = c.relname
        and c.relkind = 'r'
    order by t.table_name
"""
COLUMNS_QUERY = """
select
        column_name
    from
        information_schema.columns
    where
        table_name = '{0}'
"""

class PostgreSQLConnection(DatabaseConnection):
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

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        if self.database and self.database != '*':
            return '%s@%s/%s/' % (self.user, self.host, self.database)

        return '%s@%s/' % (self.user, self.host)

    def title(self):
        return self.autocomplete()

    def subtitle(self):
        return 'PostgreSQL Connection'

    def matches(self, options):
        return options.uri.startswith("%s@%s" % (self.user, self.host))

    def proceed(self):
        from ..dbnavigator import DatabaseNavigator
        from ..options import Options

        if Options.database == None:
            # print this connection
            DatabaseNavigator.print_connections([self])
            return

        try:
            self.connect(Options.database)

            if not Options.database or Options.table == None:
                dbs = self.databases()
                if Options.database:
                    dbs = [db for db in dbs if Options.database in db.name]

                DatabaseNavigator.print_databases(dbs)
                return

            tables = [t for k, t in self.tables().iteritems()]
            tables = sorted(tables, key=lambda t: t.name)
            if Options.table:
                ts = [t for t in tables if Options.table == t.name]
                if len(ts) == 1 and Options.filter != None:
                    table = ts[0]
                    if Options.filter and Options.display:
                        DatabaseNavigator.print_values(self, table, Options.filter)
                    else:
                        rows = table.rows(self, Options.filter)
                        DatabaseNavigator.print_rows(rows)
                    return
            
            if Options.table:
                tables = [t for t in tables if t.name.startswith(Options.table)]
            DatabaseNavigator.print_tables(tables)
        finally:
            if self.connected():
                self.close()

    def filter(self, options):
        matches = True

        if options.user:
            filter = options.user
            if options.host != None:
                matches = filter in self.user
            else:
                matches = filter in self.user or filter in self.host
        if options.host != None:
            matches = matches and options.host in self.host

        return matches

    def connect(self, database):
        logging.debug('Connecting to database %s' % database)
        
        db = None
        if database:
            try:
                db = create_engine('postgresql://%s:%s@%s/%s' % (self.user, self.password, self.host, database))
                self.con = db.connect()
                self.inspector = reflection.Inspector.from_engine(db)
            except OperationalError, e:
                db = create_engine('postgresql://%s:%s@%s/' % (self.user, self.password, self.host))
                self.con = db.connect()
                self.inspector = reflection.Inspector.from_engine(db)
                database = None

            if database:
                self.table_map = {t.name.encode('ascii'): t for t in self.tablesof(database)}
                logging.debug('Table Map: %s' % self.table_map)
                self.put_foreign_keys()
        else:
            db = create_engine('postgresql://%s:%s@%s/' % (self.user, self.password, self.host))
            self.con = db.connect()
            self.inspector = reflection.Inspector.from_engine(db)

    def connected(self):
        return self.con

    def close(self):
        self.con.close()
        self.con = None

    def cursor(self):
        return self.con

    def databases(self):
        if not self.dbs:
            query = DATABASES_QUERY
            logging.debug('Query databases: %s' % query)

            cur = self.cursor()
            start = time.time()
            result = cur.execute(query)
            logduration('Query databases', start)
    
            def d(row): return Database(self, row[0])
    
            self.dbs = map(d, result)
        
        return self.dbs

    def tables(self):
        return self.table_map

    def columns(self, table):
        logging.debug('Retrieve columns')

        query = COLUMNS_QUERY.format(table.name)
        logging.debug('Query columns: %s' % query)
        cur = self.cursor()
        start = time.time()
        result = cur.execute(query)
        logduration('Query columns', start)

        return [Column(table, row['column_name']) for row in result]

    def tablesof(self, database):
        #def t(t): return Table(self, database, t, '')
        #
        # sqlalchemy does not yet provide reflecting comments
        #tables = map(t, [t for t in self.inspector.get_table_names()])

        query = TABLES_QUERY
        logging.debug('Query tables: %s' % query)
        
        cur = self.cursor()
        start = time.time()
        result = cur.execute(query)
        logduration('Query tables', start)
        
        def t(row): return Table(self, database, row[0], row[1])
        
        return map(t, result)

    def put_foreign_keys(self):
        """Retrieves the foreign keys of the table"""
        
        for key, value in self.table_map.iteritems():
            logging.debug('Foreign keys for %s: %s' % (key, self.inspector.get_foreign_keys(value.name)))

        logging.debug('Retrieve foreign keys')
        query = FOREIGN_KEY_QUERY
        logging.debug('Query foreign keys: %s' % query)
        cur = self.cursor()
        start = time.time()
        result = cur.execute(query)
        logduration('Query foreign keys', start)
        for row in result:
            a = Column(self.table_map[row['table_name'].encode('ascii')], row['column_name'])
            b = Column(self.table_map[row['foreign_table_name'].encode('ascii')], row['foreign_column_name'])
            fk = ForeignKey(a, b)
            self.table_map[a.table.name].fks[a.name] = fk
            self.table_map[b.table.name].fks[str(a)] = fk
