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


class Table(Dto):
    def __init__(
            self,
            name=None,
            uri=None,
            owner=None,
            size=None,
            primary_key=None,
            columns=None,
            foreign_keys=None):
        self.name = name
        self.uri = uri
        self.owner = owner
        self.size = size
        self.primary_key = primary_key
        self.columns = columns
        self.foreign_keys = foreign_keys

    @staticmethod
    def from_json(d):
        return Table(
            name=from_json(d.get('name')),
            uri=from_json(d.get('uri')),
            owner=from_json(d.get('owner')),
            size=from_json(d.get('size')),
            primary_key=from_json(d.get('primary_key')),
            columns=from_json(d.get('columns')),
            foreign_keys=from_json(d.get('foreign_keys')))
