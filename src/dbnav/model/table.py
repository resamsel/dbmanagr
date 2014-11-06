#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from sqlalchemy.exc import ProgrammingError, DataError

from dbnav.model.tablecomment import TableComment
from dbnav.model.row import Row
from dbnav.querybuilder import QueryBuilder, SimplifyMapper
from dbnav.model.baseitem import BaseItem
from dbnav.comment import Comment

DEFAULT_LIMIT = 50

OPTION_URI_VALUE_FORMAT = '%s%s/?%s'

logger = logging.getLogger(__name__)


class Table(BaseItem):
    def __init__(
            self, connection, database, name, comment, owner=None, size=None):
        self.connection = connection
        self.database = database
        self.name = name
        self.entity = connection.meta.tables[name]
        self.comment = TableComment(comment)
        self.owner = owner
        self.size = size
        self.cols = None
        self.fks = {}
        self.uri = connection.autocomplete()
        self.primary_key = 'id'

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
        self.cols = connection.columns(self)

    def columns(self, connection=None, column=None):
        """Retrieves columns of table with given filter applied"""

        if not self.cols:
            if connection is None:
                connection = self.connection
            self.init_columns(connection)

        if column is None:
            return self.cols

        return [c for c in self.cols if column in c.name]

    def column(self, name):
        if not self.cols:
            self.init_columns(self.connection)

        for col in self.cols:
            if col.name == name:
                return col

        return None

    def rows(self, filter=None, limit=DEFAULT_LIMIT, simplify=False):
        """Retrieves rows from the table with the given filter applied"""

        builder = QueryBuilder(
            self.connection,
            self,
            filter=filter,
            order=self.comment.order if simplify else [],
            limit=limit,
            simplify=simplify)

        try:
            result = self.connection.queryall(
                builder.build(),
                name='Rows',
                mapper=SimplifyMapper(
                    self,
                    comment=Comment(
                        self,
                        builder.counter,
                        builder.aliases,
                        None)))
        except DataError as e:
            raise
        except ProgrammingError as e:
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
