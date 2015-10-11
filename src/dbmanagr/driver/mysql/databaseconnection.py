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

from dbmanagr.model.databaseconnection import UriDatabaseConnection

AUTOCOMPLETE_FORMAT = '{user}@{host}/{database}'


class MySQLConnection(UriDatabaseConnection):
    def __init__(self, uri, host, port, path, user, password):
        UriDatabaseConnection.__init__(
            self,
            dbms='mysql',
            database=path,
            uri=uri,
            host=host,
            port=port,
            user=user,
            password=password,
            subtitle='MySQL Connection')

    def __repr__(self):
        return AUTOCOMPLETE_FORMAT.format(
            user=self.user,
            host=self.host,
            database=self.database if self.database != '*' else ''
        )
