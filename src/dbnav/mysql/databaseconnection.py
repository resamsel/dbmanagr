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

from sqlalchemy.exc import OperationalError

from dbnav.model.databaseconnection import DatabaseConnection
from dbnav.model.database import Database

AUTOCOMPLETE_FORMAT = '{user}@{host}/{database}'

logger = logging.getLogger(__name__)


class MySQLDatabase(Database):
    def __init__(self, connection, name):
        self.connection = connection
        self.name = name

    def __repr__(self):
        return AUTOCOMPLETE_FORMAT.format(
            user=self.connection.user,
            host=self.connection.host,
            database=self.name
        )


class MySQLConnection(DatabaseConnection):
    """A database connection"""

    def __init__(self, uri, host, port, database, user, password):
        DatabaseConnection.__init__(
            self,
            dbms='mysql',
            database=database,
            uri=uri)
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.con = None

    def __repr__(self):
        return AUTOCOMPLETE_FORMAT.format(
            user=self.user,
            host=self.host,
            database=self.database if self.database != '*' else ''
        )

    def autocomplete(self):
        """Retrieves the autocomplete string"""

        if self.database and self.database != '*':
            return '%s@%s/%s/' % (self.user, self.host, self.database)

        return '%s@%s/' % (self.user, self.host)

    def title(self):
        return self.autocomplete()

    def subtitle(self):
        return 'MySQL Connection'

    def matches(self, options):
        options = options.get('mysql')
        if options.gen:
            return options.gen.startswith("%s@%s" % (self.user, self.host))
        return False

    def filter(self, options):
        options = options.get('mysql')
        matches = True

        if options.user:
            filter = options.user
            if options.host is not None:
                matches = filter in self.user
            else:
                matches = filter in self.user or filter in self.host
        if options.host is not None:
            matches = matches and options.host in self.host

        return matches

    def connect(self, database):
        logger.debug('Connecting to database %s', database)

        if database:
            try:
                self.connect_to(
                    self.uri.format(
                        user=self.user,
                        password=self.password,
                        host=self.host,
                        database=database))
                self.database = database
            except OperationalError:
                self.connect_to(
                    self.uri.format(
                        user=self.user,
                        password=self.password,
                        host=self.host,
                        database=''))
                database = None
        else:
            self.connect_to(
                self.uri.format(
                    user=self.user,
                    password=self.password,
                    host=self.host,
                    database=''))
