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

from dbmanagr.jsonable import Jsonable
from dbmanagr.utils import freeze


class Dto(Jsonable):
    def __init__(self, autocomplete=None):
        self.autocomplete_ = autocomplete

    def autocomplete(self):
        return self.autocomplete_

    def __hash__(self):
        return hash(freeze(self.__dict__))

    def __eq__(self, o):
        return hash(self) == hash(o)
