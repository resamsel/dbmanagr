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

from dbmanagr.dto import Dto
from dbmanagr.jsonable import from_json
from dbmanagr.utils import filter_keys


class Table(Dto):
    def __init__(
            self,
            name=None,
            uri=None,
            owner=None,
            size=None,
            primary_key=None,
            columns=None,
            foreign_keys=None,
            autocomplete=None):
        Dto.__init__(self, autocomplete)

        self.name = name
        self.uri = uri
        self.owner = owner
        self.size = size
        self.primary_key = primary_key
        self.columns = columns
        self.foreign_keys = foreign_keys

    def __str__(self):
        if self.uri:
            return '{}{}'.format(self.uri, self.name)
        return self.name

    @staticmethod
    def from_json(d):
        return Table(
            **from_json(
                filter_keys(
                    d,
                    'name', 'uri', 'owner', 'size', 'primary_key', 'columns',
                    'foreign_keys', 'autocomplete'
                )
            )
        )
