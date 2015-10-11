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

import logging

from os.path import basename

from dbmanagr.logger import LogWith
from dbmanagr.model.databaseconnection import DatabaseConnection
from dbmanagr.model.database import Database

AUTOCOMPLETE_FORMAT = "{connection}/"

logger = logging.getLogger(__name__)


class SQLiteDatabase(Database):
    def __init__(self, connection):
        Database.__init__(self, connection, '', AUTOCOMPLETE_FORMAT)


class SQLiteConnection(DatabaseConnection):
    def __init__(self, uri, *args):
        self.path = args[2]
        self.filename = basename(self.path)
        DatabaseConnection.__init__(
            self,
            dbms='sqlite',
            database=self.databases()[0],
            uri=uri,
            subtitle='SQLite Connection')

    def __repr__(self):
        return AUTOCOMPLETE_FORMAT.format(connection=self.filename)

    def matches(self, options):
        if options.uri:
            return options.uri.startswith(self.filename)
        return False

    def filter_(self, options):
        options = options.get(self.dbms)
        return not options.uri or options.uri in self.filename

    @LogWith(logger)
    def connect(self, database=None):
        self.connect_to(self.uri.format(file=self.path))

    def databases(self):
        return [SQLiteDatabase(self)]
