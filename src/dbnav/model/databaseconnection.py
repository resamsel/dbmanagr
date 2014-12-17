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
from sqlalchemy.engine import reflection

from dbnav.logger import LogWith
from dbnav.model import DEFAULT_LIMIT
from dbnav.model.column import create_column
from dbnav.model.baseitem import BaseItem
from dbnav.model.foreignkey import ForeignKey
from dbnav.model.database import Database
from dbnav.model.table import Table
from dbnav.model.tablecomment import TableComment

logger = logging.getLogger(__name__)


class DatabaseConnection(BaseItem):
    def __init__(self, **kwargs):
        self.dbms = kwargs.get('dbms', None)
        self.database = kwargs.get('database', None)
        self.uri = kwargs.get('uri', None)
        self._tables = kwargs.get('tables', None)
        self._comments = kwargs.get('comments', None)
        self._inspector = None
        self._meta = None

    def title(self):
        return self.__repr__()

    def subtitle(self):
        return 'Generic Connection'

    def autocomplete(self):
        return self.__repr__()

    def icon(self):
        return 'images/connection.png'

    def uri(self, table):
        return u'%s%s' % (self.autocomplete(), table)

    def matches(self, options):
        return options.arg in self.title()

    def connect(self, database):
        pass

    @LogWith(logger)
    def connect_to(self, source):
        self.engine = create_engine(source)
        self.con = self.engine.connect()

    def meta(self):
        if self._meta is None:
            self._meta = MetaData()
            self._meta.reflect(bind=self.engine)

        return self._meta

    def inspector(self):
        if self._inspector is None:
            self._inspector = reflection.Inspector.from_engine(self.engine)

        return self._inspector

    def connected(self):
        return self.con

    def close(self):
        if self.con:
            self.con.close()
            self.con = None

    def cursor(self):
        return self.con

    def begin(self):
        return self.con.begin()

    @LogWith(logger, log_args=False, log_result=False)
    def execute(self, query, name='Unnamed'):
        cur = self.cursor()

        if not cur:
            raise Exception('Database is not connected')

        return cur.execute(query)

    @LogWith(logger, log_args=False, log_result=False)
    def queryall(self, query, name='Unnamed', mapper=None):
        result = query.all()

        if mapper:
            for row in result:
                mapper.map(row)

        return result

    @LogWith(logger, log_args=False, log_result=False)
    def queryone(self, query, name='Unnamed', mapper=None):
        result = query.one()

        if mapper:
            mapper.map(result)

        return result

    def rows(self, table, filter=None, limit=DEFAULT_LIMIT, simplify=None):
        return table.rows(self, filter, limit, simplify)

    def filter(self, options):
        return True

    def databases(self):
        return map(
            lambda name: Database(self, name),
            self.inspector().get_schema_names())

    @LogWith(logger)
    def init_tables(self, database):
        self._tables = dict(map(
            lambda table: (table, Table(
                database, self.entity(table), self.autocomplete())),
            self.meta().tables))
        logger.debug('Tables: %s' % self._tables)
        self.init_foreign_keys()

    @LogWith(logger)
    def tables(self):
        if not self._tables:
            self.init_tables(self.database)

        return self._tables

    def table(self, tablename):
        return self.tables().get(tablename, None)

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
        for k, t in self.meta().tables.iteritems():
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
                self._tables[a.table.name].fks[a.name] = fk
                self._tables[b.table.name].fks[str(a)] = fk

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__repr__() == other.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    def __getstate__(self):
        state = dict(self.__dict__)
        if 'con' in state:
            del state['con']
        return state
