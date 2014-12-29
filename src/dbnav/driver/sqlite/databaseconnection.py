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

from dbnav.logger import LogWith
from dbnav.model.databaseconnection import DatabaseConnection
from dbnav.model.database import Database

AUTOCOMPLETE_FORMAT = "%s/"

logger = logging.getLogger(__name__)


class SQLiteDatabase(Database):
    def __init__(self, connection):
        self.connection = connection
        self.name = ''

    def __repr__(self):
        return AUTOCOMPLETE_FORMAT % self.connection


class SQLiteConnection(DatabaseConnection):
    """A database connection"""

    def __init__(self, uri, host, port, path, user, password):
        DatabaseConnection.__init__(
            self,
            dbms='sqlite',
            database=self.databases()[0],
            uri=uri)
        self.path = path
        self.filename = basename(self.path)
        self.con = None

    def __repr__(self):
        return AUTOCOMPLETE_FORMAT % self.filename

    def subtitle(self):
        return 'SQLite Connection'

    def matches(self, options):
        options = options.get(self.dbms)
        if options.uri:
            return options.uri.startswith(self.filename)
        return False

    def filter(self, options):
        options = options.get(self.dbms)
        return not options.uri or options.uri in self.path

    @LogWith(logger)
    def connect(self, database=None):
        self.connect_to(self.uri.format(file=self.path))

    def databases(self):
        return [SQLiteDatabase(self)]
