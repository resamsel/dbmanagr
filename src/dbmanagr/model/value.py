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

from .baseitem import BaseItem
from dbmanagr import KIND_FOREIGN_VALUE, KIND_FOREIGN_KEY, KIND_VALUE
from dbmanagr import IMAGE_FOREIGN_VALUE, IMAGE_FOREIGN_KEY, IMAGE_VALUE

TITLES = {
    KIND_FOREIGN_VALUE: u'← %s',
    KIND_FOREIGN_KEY: u'→ %s',
    KIND_VALUE: u'%s'
}
ICONS = {
    KIND_FOREIGN_VALUE: IMAGE_FOREIGN_VALUE,
    KIND_FOREIGN_KEY: IMAGE_FOREIGN_KEY,
    KIND_VALUE: IMAGE_VALUE
}


class Value(BaseItem):
    """A value from the database"""

    def __init__(self, value, subtitle, autocomplete, validity, kind):
        self._value = value
        self._subtitle = subtitle
        self._autocomplete = autocomplete
        self._validity = validity
        self._kind = kind

    def title(self):
        if type(self._value) is buffer:
            return '[BLOB]'
        return TITLES.get(self._kind, KIND_VALUE) % self._value

    def subtitle(self):
        return self._subtitle

    def autocomplete(self):
        return self._autocomplete

    def validity(self):
        return self._validity

    def icon(self):
        return ICONS.get(self._kind, KIND_VALUE)

    def value(self):
        return self._value

    def as_json(self):
        return {
            '__cls__': str(self.__class__),
            'value': self._value,
            'subtitle': self._subtitle
        }
