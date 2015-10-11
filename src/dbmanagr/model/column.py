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

from dbmanagr.model.baseitem import BaseItem
from dbmanagr.formatter import Formatter
from dbmanagr.utils import dictminus


class Column(BaseItem):
    """A table column"""

    def __init__(self, table, name, **kwargs):
        self.table = table
        self.name = name
        self.type = None
        self.nullable = None
        self.default = None
        self.__dict__.update(kwargs)
        self.tablename = table.name
        self.uri = self.autocomplete()

    def __repr__(self):
        return '%s.%s' % (self.table.name, self.name)

    def __str__(self):
        return self.__repr__()

    def ddl(self):
        return '{0} {1}{2}{3}'.format(
            self.name,
            self.type.compile(),
            {False: ' not null'}.get(self.nullable, ''),
            {None: ''}.get(self.default, ' default {0}'.format(self.default)))

    def title(self):
        return self.name

    def subtitle(self):
        return self.table.title()

    def autocomplete(self):
        return '%s%s?%s' % (self.table.uri, self.table.name, self.name)

    def icon(self):
        return 'images/table.png'

    def format(self):
        return Formatter.format_column(self)

    def as_json(self):
        d = {
            '__cls__': str(self.__class__),
            'name': self.name,
            'table': self.table.name,
            'type': self.type.compile(),
            'uri': self.uri
        }
        if self.default is not None:
            d['default'] = self.default
        return d


def create_column(table, name, column=None):
    if column is None:
        return Column(table, name)
    return Column(table, name, **dictminus(column.__dict__, 'name', 'table'))
