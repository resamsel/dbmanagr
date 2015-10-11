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


class ForeignKey(Dto):
    def __init__(self, a=None, b=None):
        Dto.__init__(self)

        self.a = a
        self.b = b

    def __str__(self):
        return '{a} -> {b}'.format(a=self.a, b=self.b)

    @staticmethod
    def from_json(d):
        return ForeignKey(
            a=from_json(d.get('a')),
            b=from_json(d.get('b'))
        )
