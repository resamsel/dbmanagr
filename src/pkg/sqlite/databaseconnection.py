#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import logging
import sqlite3
import time

from os.path import expanduser, basename

from ..logger import logduration
from ..model.databaseconnection import *
from ..model.database import *
from ..model.table import *
from ..model.column import *
from ..model.foreignkey import *

CACHE_TIME = 2*60
TABLES_QUERY = """
select
        name as tbl, '' as comment
    from
        sqlite_master
    where
        type = 'table'
    order by name
"""
COLUMNS_QUERY = """
pragma table_info({0})
"""

class SQLiteConnection(DatabaseConnection):
    """A database connection"""

    def __init__(self, path):
        self.path = path
        self.filename = basename(self.path)
        self.con = None
        self.dbs = None
        self.tbls = None

    def __repr__(self):
        return self.filename

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        return self.filename

    def title(self):
        return self.filename

    def subtitle(self):
        return 'SQLite Connection'

    def matches(self, options):
        logging.debug('SQLite matches')
        return options.arg.startswith(self.filename)

    def filter(self, options):
        return not options.arg or options.arg in self.path

    def proceed(self):
        logging.debug('SQLite proceed')

        from ..dbnavigator import DatabaseNavigator
        from ..options import Options

        if len(Options.paths) > 1: Options.table = Options.paths[1]
        if len(Options.paths) > 2: Options.filter = Options.paths[2]
        Options.display = len(Options.paths) > 3

        try:
            self.connect()

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

    def connect(self, database=None):
        logging.debug('Connecting to database %s' % database)
        
        self.con = sqlite3.connect(self.path)
        self.con.row_factory = sqlite3.Row

        self.table_map = {t.name: t for t in self.tablesof(database)}

    def connected(self):
        return self.con

    def close(self):
#        self.con.close()
        self.con = None

    def cursor(self):
        return self.con.cursor()

    def databases(self):
        logging.debug('Retrieve databases')
        return [Database(self, '_')]

    def tables(self):
        return self.table_map
    
    def columns(self, table):
        query = COLUMNS_QUERY.format(table.name)
        cur = self.cursor()
        cur.execute(query)
        
        return [Column(table, c['name'], c['pk']) for c in cur.fetchall()]

    def tablesof(self, database):
        if not self.tbls:
            query = TABLES_QUERY
            logging.debug('Query tables: %s' % query)
    
            cur = self.cursor()
            start = time.time()
            cur.execute(query)
            logduration('Query tables', start)
    
            def t(row): return Table(self, database, row[0], row[1])
    
            self.tbls = map(t, cur.fetchall())

        return self.tbls
