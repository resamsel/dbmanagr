#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sqlalchemy.exc import ProgrammingError, DataError

from dbnav.querybuilder import QueryBuilder, SimplifyMapper
from dbnav.comment import create_comment
from dbnav.exception import UnknownColumnException
from dbnav.model.row import Row
from dbnav.model.baseitem import BaseItem

DEFAULT_LIMIT = 50

OPTION_URI_VALUE_FORMAT = '%s%s/?%s'

logger = logging.getLogger(__name__)


class Table(BaseItem):
    def __init__(
            self, connection, database, name, owner=None, size=None):
        self.connection = connection
        self.database = database
        self.name = name
        self.entity = connection.entity(name)
        self.owner = owner
        self.size = size
        self._columns = None
        self.fks = {}
        self.uri = connection.autocomplete()
        self.primary_key = None

    def __repr__(self):
        return self.name

    def autocomplete(
            self, column=None, value=None, format=OPTION_URI_VALUE_FORMAT):
        """Retrieves the autocomplete string for the given column and value"""

        if column is None:
            return u'%s%s?' % (self.uri, self.name)

        tablename = self.name
        if type(value) is buffer:
            value = '[BLOB]'
        else:
            value = u'%s=%s' % (column, value)

        return format % (self.uri, tablename, value)

    def init_columns(self, connection):
        self._columns = connection.columns(self)

    def columns(self, connection=None, column=None):
        """Retrieves columns of table with optional filter applied"""

        if not self._columns:
            if connection is None:
                connection = self.connection
            self.init_columns(connection)

        if column is None:
            return self._columns

        return filter(lambda c: column in c.name, self._columns)

    def column(self, name):
        if not self._columns:
            self.init_columns(self.connection)

        if type(name) is int:
            return self._columns[name]

        for col in self._columns:
            if col.name == name:
                return col

        return None

    def rows(self, filter=None, limit=DEFAULT_LIMIT, simplify=None):
        """Retrieves rows from the table with the given filter applied"""
        logger.debug(
            'table.rows(self=%s, filter=%s, limit=%s, simplify=%s)',
            self, filter, limit, simplify)

        if simplify is None:
            simplify = False

        builder = QueryBuilder(
            self.connection,
            self,
            filter=filter,
            order=self.connection.comment(self.name).order if simplify else [],
            limit=limit,
            simplify=simplify)

        mapper = None
        if simplify:
            mapper = SimplifyMapper(
                self,
                comment=create_comment(
                    self,
                    self.connection.comment(self.name),
                    builder.counter,
                    builder.aliases,
                    None))

        try:
            result = self.connection.queryall(
                builder.build(),
                name='Rows',
                mapper=mapper)
        except DataError as e:
            raise
        except ProgrammingError as e:
            raise
        except UnknownColumnException as e:
            raise
        except BaseException as e:
            logger.error(e, exc_info=1)
            import sys
            raise type(e), type(e)(
                '{} (check comment on table {})'.format(e.message, self.name)
            ), sys.exc_info()[2]

        return map(lambda row: Row(self.connection, self, row), result)

    def foreign_keys(self):
        return self.fks

    def foreign_key(self, name):
        if name in self.fks:
            return self.fks[name]
        return None

    def title(self):
        return self.name

    def subtitle(self):
        if self.owner and self.size:
            return u'Owner: %s (%s)' % (self.owner, self.size)
        return u'Table'

    def icon(self):
        return 'images/table.png'

    def escaped(self, f):
        return dict(
            map(
                lambda (k, v): (k.encode('ascii', 'ignore'), f(v)),
                self.__dict__.iteritems()))
