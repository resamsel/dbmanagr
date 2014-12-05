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

OPTION_URI_DATABASE_FORMAT = '%s/'


class Database(BaseItem):
    """The database used with the given connection"""

    def __init__(self, connection, name):
        self.connection = connection
        self.name = name

    def __repr__(self):
        return '{user}@{host}/{database}'.format(
            user=self.connection.user,
            host=self.connection.host,
            database=self.name)

    def title(self):
        return self.autocomplete()

    def subtitle(self):
        return 'Database'

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        return OPTION_URI_DATABASE_FORMAT % (self.__repr__())

    def icon(self):
        return 'images/database.png'
