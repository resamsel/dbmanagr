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
from dbnav.utils import filter_keys


class Column(Dto):
    def __init__(
            self,
            name=None,
            tablename=None,
            type=None,
            nullable=None,
            default=None,
            autoincrement=None,
            primary_key=None,
            title=None,
            subtitle=None,
            autocomplete=None):
        Dto.__init__(self, title, subtitle, autocomplete)

        self.name = name
        self.tablename = tablename
        self.autocomplete_ = autocomplete
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
            {None: ''}.get(self.autocomplete_, ' autoincrement {0}'.format(
                self.autoincrement)))

    def autocomplete(self):
        return self.autocomplete_

    @staticmethod
    def from_json(d):
        return Column(
            **from_json(
                filter_keys(
                    d,
                    'name', 'tablename', 'type', 'nullable', 'default',
                    'autoincrement', 'primary_key', 'title', 'subtitle',
                    'autocomplete'
                )
            )
        )
