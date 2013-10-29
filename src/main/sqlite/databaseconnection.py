#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import logging
import time

from sqlalchemy import *
from sqlalchemy.engine import reflection
from os.path import expanduser, basename

from ..logger import logduration
from ..model.databaseconnection import *
from ..model.database import *
from ..model.table import *
from ..model.column import *
from ..model.foreignkey import *
from ..options import *

CACHE_TIME = 2*60
COLUMNS_QUERY = """
pragma table_info({0})
"""

logger = logging.getLogger(__name__)

class SQLiteConnection(DatabaseConnection):
    """A database connection"""

    def __init__(self, path):
        DatabaseConnection.__init__(self)
        self.path = path
        self.filename = basename(self.path)
        self.con = None
        self.dbs = None
        self.database = self.databases()[0]
        self.tbls = None

    def __repr__(self):
        return self.filename

    def autocomplete(self):
        return self.filename

    def title(self):
        return self.filename

    def subtitle(self):
        return 'SQLite Connection'

    def matches(self, options):
        options = Options.parser['sqlite']
        if options.uri:
            return options.uri.startswith(self.filename)
        return False

    def filter(self, options):
        options = Options.parser['sqlite']
        return not options.uri or options.uri in self.path

    def proceed(self):
        from ..dbnavigator import DatabaseNavigator

        options = Options.parser['sqlite']

        try:
            self.connect()

            if options.showcolumns:
                table = self.tables()[options.table]
                if options.showcolumns and options.filter == None:
                    columns = table.columns(self, options.column)
                    DatabaseNavigator.print_columns(columns)
                elif options.showvalues:
                    DatabaseNavigator.print_values(self, table, '%s=%s' % (options.column, options.filter))
                else:
                    rows = table.rows(self, options.filter)
                    DatabaseNavigator.print_rows(rows)
                return

            tables = [t for k, t in self.tables().iteritems()]
            tables = sorted(tables, key=lambda t: t.name)

            if options.table:
                tables = [t for t in tables if t.name.startswith(options.table)]

            DatabaseNavigator.print_tables(tables)
        finally:
            self.close()

    def connect(self, database=None):
        logger.debug('Connecting to database %s' % database)
        
        db = create_engine('sqlite+pysqlite:///%s' % self.path)
        self.con = db.connect()
        self.inspector = reflection.Inspector.from_engine(db)

    def databases(self):
        logger.debug('Retrieve databases')
        return [Database(self, '_')]

    def tablesof(self, database):
        def t(name): return Table(self, database, name, '')

        return map(t, [t for t in self.inspector.get_table_names()])
