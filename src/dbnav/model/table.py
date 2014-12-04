#!/usr/bin/env python
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

from sqlalchemy.exc import ProgrammingError, DataError

from dbnav.logger import LogWith
from dbnav.querybuilder import QueryBuilder, SimplifyMapper
from dbnav.comment import create_comment
from dbnav.exception import UnknownColumnException
from dbnav.model.baseitem import BaseItem
from dbnav.model.column import create_column
from dbnav.model.row import Row
from dbnav.model import DEFAULT_LIMIT

OPTION_URI_VALUE_FORMAT = '%s%s/?%s'

logger = logging.getLogger(__name__)


class Table(BaseItem):
    def __init__(
            self, database, entity, uri, owner=None, size=None):
        self.database = database
        self.name = entity.name
        self.entity = entity
        self.uri = uri
        self.owner = owner
        self.size = size

        self._columns = map(
            lambda c: create_column(self, str(c.name), c),
            entity.columns)
        self.fks = {}

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

    def columns(self, needle=None):
        """Retrieves columns of table with optional filter applied"""

        if needle is None:
            return self._columns

        return filter(lambda c: needle in c.name, self._columns)

    def column(self, name):
        if type(name) is int:
            return self._columns[name]

        for col in self._columns:
            if col.name == name:
                return col

        return None

    @LogWith(logger, log_result=False, log_args=False)
    def rows(
            self, connection, filter=None, limit=DEFAULT_LIMIT, simplify=None):
        """Retrieves rows from the table with the given filter applied"""

        comment = None
        order = []

        if simplify is None:
            simplify = False

        if simplify:
            comment = connection.comment(self.name)
            order = comment.order

        builder = QueryBuilder(
            connection,
            self,
            filter=filter,
            order=order,
            limit=limit,
            simplify=simplify)

        mapper = None
        if simplify:
            mapper = SimplifyMapper(
                self,
                comment=create_comment(
                    self,
                    comment,
                    builder.counter,
                    builder.aliases,
                    None))

        try:
            result = connection.queryall(
                builder.build(),
                name='Rows',
                mapper=mapper)
        except (DataError, ProgrammingError, UnknownColumnException,
                UnicodeEncodeError):
            raise
        except BaseException as e:
            logger.error(e, exc_info=1)
            import sys
            raise type(e), type(e)(
                u'{} (check comment on table {})'.format(e.message, self.name)
            ), sys.exc_info()[2]

        return map(lambda row: Row(self, row), result)

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
