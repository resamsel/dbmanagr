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

OPTION_URI_DATABASE_FORMAT = '{}/'
AUTOCOMPLETE_FORMAT = '{connection.user}@{connection.host}/{database}'


class Database(BaseItem):
    """The database used with the given connection"""

    def __init__(
            self,
            connection,
            name,
            autocomplete_format=AUTOCOMPLETE_FORMAT):
        self._connection = connection
        self.name = name
        self._autocomplete_format = autocomplete_format
        self.uri = repr(self)

    def __repr__(self):
        return self._autocomplete_format.format(
            connection=self._connection,
            database=self.name)

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        return OPTION_URI_DATABASE_FORMAT.format(self.uri)
