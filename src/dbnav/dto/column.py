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

from dbnav.dto import Dto
from dbnav.jsonable import from_json


class Column(Dto):
    def __init__(
            self,
            name=None,
            tablename=None,
            autocomplete=None,
            type=None,
            nullable=None,
            default=None,
            autoincrement=None,
            primary_key=None):
        self.name = name
        self.tablename = tablename
        self.autocomplete = autocomplete
        self.type = type
        self.nullable = nullable
        self.default = default
        self.autoincrement = autoincrement
        self.primary_key = primary_key

    def __str__(self):
        if self.tablename:
            return '%s.%s' % (self.tablename, self.name)
        return self.name

    def ddl(self):
        return '{0} {1}{2}{3}'.format(
            self.name,
            self.type,
            {False: ' not null'}.get(self.nullable, ''),
            {None: ''}.get(self.default, ' default {0}'.format(self.default)),
            {None: ''}.get(self.autocomplete, ' autoincrement {0}'.format(
                self.autoincrement)))

    @staticmethod
    def from_json(d):
        return Column(
            name=from_json(d.get('name')),
            tablename=from_json(d.get('tablename')),
            autocomplete=from_json(d.get('autocomplete')),
            type=from_json(d.get('type')),
            nullable=from_json(d.get('nullable')),
            default=from_json(d.get('default')),
            autoincrement=from_json(d.get('autoincrement')),
            primary_key=from_json(d.get('primary_key'))
        )
