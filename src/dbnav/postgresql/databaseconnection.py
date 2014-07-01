#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import logging

from sqlalchemy.exc import OperationalError
from os.path import expanduser

from ..model.databaseconnection import *
from ..model.database import *
from ..model.table import *
from ..model.column import *
from ..model.foreignkey import *
from ..options import Options

CACHE_TIME = 2*60
DATABASES_QUERY = """
select
        datname as database_name
    from
        pg_database
    where
        datistemplate = false
        and pg_catalog.pg_get_userbyid(datdba) = '%s'
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
AUTOCOMPLETE_FORMAT = '%s@%s/%s'

logger = logging.getLogger(__name__)

class PostgreSQLDatabase(Database):
    def __init__(self, connection, name):
        self.connection = connection
        self.name = name
    def __repr__(self):
        return AUTOCOMPLETE_FORMAT % (self.connection.user, self.connection.host, self.name)

class PostgreSQLConnection(DatabaseConnection):
    """A database connection"""

    def __init__(self, host, port, database, user, password):
        DatabaseConnection.__init__(self)
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.con = None
        self.dbs = None
        self.tbls = {}
        self.driver = 'postgresql'

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
        options = options.get(self.driver)
        if options.gen:
            return options.gen.startswith("%s@%s" % (self.user, self.host))
        return False

    def filter(self, options):
        options = options.get(self.driver)
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
        logger.debug('Connecting to database %s' % database)
        
        if database:
            try:
                self.connect_to('postgresql://%s:%s@%s/%s' % (self.user, self.password, self.host, database))
                self.database = database
            except OperationalError, e:
                self.connect_to('postgresql://%s:%s@%s/' % (self.user, self.password, self.host))
                database = None
        else:
            self.connect_to('postgresql://%s:%s@%s/' % (self.user, self.password, self.host))

    def databases(self):
        # does not yet work with sqlalchemy...
        if not self.dbs:
            result = self.execute(DATABASES_QUERY % self.user, 'Databases')
    
            def d(row): return PostgreSQLDatabase(self, row[0])
    
            self.dbs = map(d, result)
        
        return self.dbs

    def tablesof(self, database):
        ## sqlalchemy does not yet provide reflecting comments
        #tables = [Table(self, database, t, '') for t in self.inspector.get_table_names()]

        result = self.execute(TABLES_QUERY, 'Tables')

        def t(row): return Table(self, database, row[0], row[1])

        return map(t, result)

    def put_foreign_keys(self):
        """Retrieves the foreign keys of the table"""
        
        result = self.execute(FOREIGN_KEY_QUERY, 'Foreign Keys')

        for row in result:
            a = Column(self.tbls[row['table_name'].encode('ascii')], row['column_name'])
            b = Column(self.tbls[row['foreign_table_name'].encode('ascii')], row['foreign_column_name'])
            fk = ForeignKey(a, b)
            self.tbls[a.table.name].fks[a.name] = fk
            self.tbls[b.table.name].fks[str(a)] = fk
