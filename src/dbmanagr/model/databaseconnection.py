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

import logging

from sqlalchemy import create_engine, MetaData
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import reflection

from dbmanagr.logger import LogWith, LogTimer
from dbmanagr.model import DEFAULT_LIMIT
from dbmanagr.model.column import create_column
from dbmanagr.model.baseitem import BaseItem
from dbmanagr.model.foreignkey import ForeignKey
from dbmanagr.model.database import Database
from dbmanagr.model.table import Table
from dbmanagr.model.tablecomment import TableComment
from dbmanagr.utils import escape_statement

logger = logging.getLogger(__name__)


class DatabaseConnection(BaseItem):
    def __init__(self, **kwargs):
        self.dbms = kwargs.get('dbms', None)
        self.database = kwargs.get('database', None)
        self.uri = kwargs.get('uri', None)
        self._subtitle = kwargs.get('subtitle', 'Generic Connection')
        self._tables = kwargs.get('tables', None)
        self._comments = kwargs.get('comments', None)
        self._engine = None
        self._inspector = None
        self._meta = None
        self._con = None

    def title(self):
        return self.__repr__()

    def subtitle(self):
        return self._subtitle

    def autocomplete(self):
        return self.__repr__()

    def icon(self):
        return 'images/connection.png'

    def matches(self, options):  # pragma: no cover
        pass

    def connect(self, database):  # pragma: no cover
        """Is to be implemented by subclasses"""

        pass

    @LogWith(logger)
    def connect_to(self, source):
        self._engine = create_engine(source)
        self._con = self._engine.connect()

    def engine(self):
        return self._engine

    def meta(self):
        if self._meta is None:
            self._meta = MetaData()
            self._meta.reflect(bind=self._engine)

        return self._meta

    def inspector(self):
        if self._inspector is None:
            self._inspector = reflection.Inspector.from_engine(self._engine)

        return self._inspector

    def connected(self):
        return self._con is not None

    def close(self):
        if self._con:
            self._con.close()
            self._con = None

    def cursor(self):
        return self._con

    def begin(self):
        return self._con.begin()

    @LogWith(logger, log_args=False, log_result=False)
    def execute(self, query):
        cur = self.cursor()
        if not cur:
            raise Exception('Database is not connected')

        timer = LogTimer(logger, 'Execution', 'Executing:\n%s', query)
        try:
            return cur.execute(escape_statement(query))
        finally:
            timer.stop()

    @LogWith(logger, log_args=False, log_result=False)
    def queryall(self, query, mapper=None):
        timer = LogTimer(logger, 'Query all', 'Querying all:\n%s', query)
        result = query.all()
        timer.stop()

        if mapper:
            for row in result:
                mapper.map(row)

        return result

    @LogWith(logger, log_args=False, log_result=False)
    def queryone(self, query, mapper=None):
        timer = LogTimer(logger, 'Query one', 'Querying one:\n%s', query)
        result = query.one()
        timer.stop()

        if mapper:
            mapper.map(result)

        return result

    def rows(self, table, filter_=None, limit=DEFAULT_LIMIT, simplify=None):
        return table.rows(self, filter_, limit, simplify)

    def filter_(self, options):
        pass

    def databases(self):
        return map(
            lambda name: Database(self, name),
            self.inspector().get_schema_names())

    @LogWith(logger)
    def init_tables(self):
        self._tables = dict(map(
            lambda table: (table, Table(
                self.entity(table), self.autocomplete())),
            self.meta().tables))
        logger.debug('Tables: %s', self._tables)
        self.init_foreign_keys()

    @LogWith(logger)
    def tables(self):
        if not self._tables:
            self.init_tables()

        return self._tables

    def table(self, tablename):
        return self.tables().get(tablename)

    def entity(self, tablename):
        return self.meta().tables[tablename]

    def init_comments(self):
        self._comments = dict(map(
            lambda k: (k, TableComment('')),
            self.tables().keys()))
        comment = self.table('_comment')
        if comment:
            # Table _comments exists, query it
            for row in self.rows(comment, limit=-1, simplify=False):
                self._comments[row['table']] = TableComment(row['comment'])

    def comments(self):
        if not self._comments:
            self.init_comments()

        return self._comments

    def comment(self, tablename):
        return self.comments().get(tablename, None)

    def init_foreign_keys(self):
        for _, t in self.meta().tables.iteritems():
            for _fk in t.foreign_keys:
                a = create_column(
                    self._tables[_fk.parent.table.name],
                    str(_fk.parent.key),
                    _fk.parent)
                b = create_column(
                    self._tables[_fk.column.table.name],
                    str(_fk.column.key),
                    _fk.column)
                fk = ForeignKey(a, b)
                self._tables[a.table.name].set_foreign_key(a.name, fk)
                self._tables[b.table.name].set_foreign_key(str(a), fk)

    def __repr__(self):  # pragma: no cover
        raise Exception('Should be overridden in subclass')

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):  # pragma: no cover
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())


class UriDatabaseConnection(DatabaseConnection):
    def __init__(self, **kwargs):
        DatabaseConnection.__init__(self, **kwargs)
        self.user = kwargs.get('user', None)
        self.password = kwargs.get('password', None)
        self.host = kwargs.get('host', None)
        self.database = kwargs.get('database', None)

    @LogWith(logger)
    def connect(self, database):
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

    def title(self):
        return self.autocomplete()

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        if self.database and self.database != '*':
            return '%s@%s/%s/' % (self.user, self.host, self.database)

        return '%s@%s/' % (self.user, self.host)

    def matches(self, options):
        if options.gen:
            return options.gen.startswith("%s@%s" % (self.user, self.host))
        return False

    def filter_(self, options):
        options = options.get(self.dbms)
        matches = True

        if options.user:
            filter_ = options.user
            if options.host is not None:
                matches = filter_ in self.user
            else:
                matches = filter_ in self.user or filter_ in self.host
        if options.host is not None:
            matches = matches and options.host in self.host

        return matches
