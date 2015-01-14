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
    def __init__(self, name=None, tablename=None, type=None, primary_key=None):
        self.name = name
        self.tablename = tablename
        self.type = type
        self.primary_key = primary_key

    @staticmethod
    def from_json(d):
        return Column(
            name=from_json(d.get('name')),
            tablename=from_json(d.get('tablename')),
            type=from_json(d.get('type')),
            primary_key=from_json(d.get('primary_key'))
        )
