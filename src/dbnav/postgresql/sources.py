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

import xml.etree.ElementTree as ET
from urlparse import urlparse
from plistlib import readPlist
from os.path import isfile

from dbnav.sources import Source
from .databaseconnection import PostgreSQLConnection

logger = logging.getLogger(__name__)


class PgpassSource(Source):
    def __init__(self, driver, file):
        Source.__init__(self)
        self.driver = driver
        self.file = file

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            with open(self.file) as f:
                pgpass = f.readlines()

            for line in pgpass:
                connection = PostgreSQLConnection(
                    self.driver, *line.strip().split(':'))
                self.connections.append(connection)

        return self.connections


class DBExplorerPostgreSQLSource(Source):
    def __init__(self, driver, file):
        Source.__init__(self)
        self.driver = driver
        self.file = file

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            try:
                tree = ET.parse(self.file)
            except Exception as e:
                logger.warn(
                    'Error parsing dbExplorer config file: %s', e.message)
                return []
            root = tree.getroot()
            for c in root.iter('connection'):
                url = urlparse(c.find('url').text.replace('jdbc:', ''))
                if url.scheme == 'postgresql':
                    host = url.netloc
                    port = 5432
                    database = '*'
                    user = c.find('user').text
                    password = c.find('password').text
                    connection = PostgreSQLConnection(
                        self.driver, host, port, database, user, password)
                    self.connections.append(connection)

        return self.connections


class NavicatPostgreSQLSource(Source):
    def __init__(self, driver, file):
        Source.__init__(self)
        self.driver = driver
        self.file = file

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            plist = readPlist(self.file)

            if 'PostgreSQL' in plist:
                for k, v in plist['PostgreSQL']['servers'].items():
                    # The key is a big problem here: it is encrypted
                    connection = PostgreSQLConnection(
                        self.driver, v['host'], v['port'],
                        v['defaultdatabase'], v['username'], v['key'])
                    self.connections.append(connection)

        return self.connections
