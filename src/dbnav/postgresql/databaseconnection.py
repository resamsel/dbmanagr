#!/usr/bin/env python
# -*- coding: utf-8 -*-

# import shelve
import logging

from sqlalchemy.exc import OperationalError

from dbnav.logger import LogWith
from dbnav.model.databaseconnection import DatabaseConnection
from dbnav.model.database import Database
from dbnav.model.table import Table
from dbnav.model.tablecomment import TableComment

DATABASES_QUERY = """
select
        db.datname as database_name
    from
        pg_database db,
        pg_roles r
    where
        db.datistemplate = false
        and r.rolname = '%s'
        and (
            r.rolsuper
            or pg_catalog.pg_get_userbyid(db.datdba) = r.rolname
        )
    order by 1"""
TABLES_QUERY = """
select
        t.table_name as tbl,
        obj_description(c.oid) as comment,
        pg_catalog.pg_get_userbyid(c.relowner) as owner,
        pg_size_pretty(pg_total_relation_size(io.relid)) as size
    from
        information_schema.tables t,
        pg_class c,
        pg_catalog.pg_statio_user_tables io
    where
        t.table_schema = 'public'
        and t.table_name = c.relname
        and io.relname = t.table_name
        and c.relkind = 'r'
    order by t.table_name"""
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
        return AUTOCOMPLETE_FORMAT % (
            self.connection.user, self.connection.host, self.name
        )


class PostgreSQLConnection(DatabaseConnection):
    """A database connection"""

    def __init__(self, uri, host, port, database, user, password):
        DatabaseConnection.__init__(
            self,
            dbms='postgresql',
            database=database,
            uri=uri)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.con = None
        self._databases = None

    def __repr__(self):
        return '%s@%s/%s' % (
            self.user, self.host, self.database if self.database != '*' else ''
        )

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
        options = options.get(self.dbms)
        if options.gen:
            return options.gen.startswith("%s@%s" % (self.user, self.host))
        return False

    def filter(self, options):
        options = options.get(self.dbms)
        matches = True

        if options.user:
            filter = options.user
            if options.host is not None:
                matches = filter in self.user
            else:
                matches = filter in self.user or filter in self.host
        if options.host is not None:
            matches = matches and options.host in self.host

        return matches

    def connect(self, database):
        logger.debug('Connecting to database %s' % database)

        if database:
            try:
                self.connect_to(
                    self.uri.format(
                        user=self.user,
                        password=self.password,
                        host=self.host,
                        database=database))
                self.database = database
            except OperationalError:
                self.connect_to(
                    self.uri.format(
                        user=self.user,
                        password=self.password,
                        host=self.host,
                        database=''))
                database = None
        else:
            self.connect_to(
                self.uri.format(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    database=''))

    def databases(self):
        # does not yet work with sqlalchemy...
        if not self._databases:
            self._databases = map(
                lambda row: PostgreSQLDatabase(self, row[0]),
                self.execute(DATABASES_QUERY % self.user, 'Databases'))

        return self._databases

    @LogWith(logger)
    def init_tables(self, database):
        # sqlalchemy does not yet provide reflecting comments

        result = self.execute(TABLES_QUERY, 'Tables')

        self._tables = {}
        self._comments = {}
        for row in result:
            self._tables[row[0]] = Table(
                database,
                self.entity(row[0]),
                self.autocomplete(),
                row[2],
                row[3])
            self._comments[row[0]] = TableComment(row[1])

        self.init_foreign_keys()
