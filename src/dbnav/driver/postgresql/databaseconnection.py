# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

# import shelve
import logging

from dbnav.logger import LogWith
from dbnav.model.databaseconnection import UriDatabaseConnection
from dbnav.model.database import Database
from dbnav.model.table import Table
from dbnav.model.tablecomment import TableComment

DATABASES_QUERY = """select
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
TABLES_QUERY = """select
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

logger = logging.getLogger(__name__)


class PostgreSQLConnection(UriDatabaseConnection):
    def __init__(self, uri, host, port, path, user, password):
        UriDatabaseConnection.__init__(
            self,
            dbms='postgresql',
            database=path,
            uri=uri,
            host=host,
            port=port,
            user=user,
            password=password)
        self._databases = None

    def __repr__(self):
        return '%s@%s/%s' % (
            self.user, self.host, self.database if self.database != '*' else ''
        )

    def subtitle(self):
        return 'PostgreSQL Connection'

    def databases(self):
        # does not yet work with sqlalchemy...
        if self._databases is None:
            self._databases = map(
                lambda row: Database(self, row[0]),
                self.execute(DATABASES_QUERY % self.user, 'Databases'))

        return self._databases

    @LogWith(logger)
    def init_tables(self, database):
        # sqlalchemy does not yet provide reflecting comments

        self._tables = {}
        self._comments = {}

        result = self.execute(TABLES_QUERY, 'Tables')
        for row in result:  # pragma: no cover
            self._tables[row[0]] = Table(  # pragma: no cover
                database,
                self.entity(row[0]),
                self.autocomplete(),
                row[2],
                row[3])
            self._comments[row[0]] = TableComment(row[1])  # pragma: no cover

        self.init_foreign_keys()  # pragma: no cover
