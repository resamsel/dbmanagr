#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from sqlalchemy import *
from sqlalchemy.engine import reflection

from ..logger import *
from ..options import Options
from .column import *

logger = logging.getLogger(__name__)

class Row:
    columns = {'id': 1, 'title': 'Title', 'subtitle': 'Subtitle', 'column_name': 'column', 0: '0', 1: '1', 'column': 'col'}
    def __init__(self, *args):
        if len(args) > 0:
            self.columns = args[0]
            if 'id' not in self.columns:
                self.columns['id'] = 0
        else:
            self.columns = Row.columns
    def __getitem__(self, i):
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

class DatabaseConnection:
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

    def matches(self, options):
        return options.arg in self.title()

    def proceed(self):
        from ..dbnavigator import DatabaseNavigator

        options = Options.parser[self.driver]

        if options.show == 'connections':
            # print this connection
            return DatabaseNavigator.print_connections([self])

        try:
            self.connect(options.database)

            if options.show == 'databases':
                dbs = self.databases()
                if options.database:
                    dbs = [db for db in dbs if options.database in db.name]

                return DatabaseNavigator.print_databases(dbs)

            if options.show == 'tables':
                tables = [t for k, t in self.tables().iteritems()]
                if options.table:
                    tables = [t for t in tables if t.name.startswith(options.table)]

                return DatabaseNavigator.print_tables(sorted(tables, key=lambda t: t.name))

            table = self.tables()[options.table]
            if options.show == 'columns':
                if options.filter == None:
                    return DatabaseNavigator.print_columns(table.columns(self, options.column))
                else:
                    return DatabaseNavigator.print_rows(table.rows(self, options))
            
            if options.show == 'values':
                return DatabaseNavigator.print_values(self, table, options)
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
            #logger.debug('Table Map: %s' % self.tbls)
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
        
        return [Column(table, col['name'], [col['name']] == pks) for col in cols]

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
