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

from dbmanagr.logger import LogWith
from dbmanagr.querybuilder import QueryBuilder, SimplifyMapper
from dbmanagr.comment import create_comment
from dbmanagr.exception import UnknownColumnException
from dbmanagr.model.baseitem import BaseItem
from dbmanagr.model.column import create_column
from dbmanagr.model.row import Row
from dbmanagr.model import DEFAULT_LIMIT

OPTION_URI_VALUE_FORMAT = '%s%s/?%s'

logger = logging.getLogger(__name__)


class Table(BaseItem):
    def __init__(
            self,
            entity=None,
            uri=None,
            owner=None,
            size=None,
            name=None,
            primary_key=None,
            columns=None):
        self.name = None
        if entity is not None:
            self.name = entity.name
        elif name is not None:
            self.name = name
        self._entity = entity
        self.uri = uri
        self.owner = owner
        self.size = size

        if entity is not None:
            self._columns = map(
                lambda c: create_column(self, str(c.name), c), entity.columns)
        elif columns is not None:
            self._columns = map(
                lambda c: create_column(self, c), columns)
        else:
            self._columns = None
        self._fks = {}

        self.primary_key = primary_key

    def __repr__(self):
        return self.name

    def autocomplete(self):
        return self.autocomplete_()

    def autocomplete_(
            self, column=None, value=None, format_=OPTION_URI_VALUE_FORMAT):
        """Retrieves the autocomplete string for the given column and value"""

        if column is None:
            return u'%s%s?' % (self.uri, self.name)

        tablename = self.name
        if type(value) is buffer:
            value = '[BLOB]'
        else:
            value = u'%s=%s' % (column, value)

        return format_ % (self.uri, tablename, value)

    def entity(self):
        return self._entity

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
            self,
            connection,
            filter_=None,
            limit=DEFAULT_LIMIT,
            simplify=None):
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
            filter_=filter_,
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
                mapper=mapper)
        except (DataError, ProgrammingError, UnknownColumnException,
                UnicodeEncodeError):  # pragma: no cover
            raise
        except BaseException as e:  # pragma: no cover
            logger.error(e, exc_info=1)  # pragma: no cover
            import sys  # pragma: no cover
            # pylint: disable=raising-non-exception
            raise type(e), type(e)(
                u'{} (check comment on table {})'.format(e.message, self.name)
            ), sys.exc_info()[2]  # pragma: no cover

        return map(lambda row: Row(self, row), result)

    def foreign_keys(self):
        return self._fks

    def foreign_key(self, name):
        if name in self._fks:
            return self._fks[name]
        return None

    def set_foreign_key(self, name, value):
        self._fks[name] = value

    def title(self):
        return self.name

    def subtitle(self):
        if self.owner and self.size:
            return u'Owner: %s (%s)' % (self.owner, self.size)
        return u'Table'
