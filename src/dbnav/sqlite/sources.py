#!/usr/bin/env python
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
from .databaseconnection import SQLiteConnection

logger = logging.getLogger(__name__)


class DBExplorerSQLiteSource(Source):
    def __init__(self, uri, file):
        logger.debug("DBExplorerSQLiteSource.__init__(%s)", file)
        Source.__init__(self)
        self.uri = uri
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
                if url.scheme == 'sqlite':
                    logger.debug("Found connection: %s", url)
                    connection = SQLiteConnection(self.uri, url.path)
                    self.connections.append(connection)

        return self.connections


class NavicatSQLiteSource(Source):
    def __init__(self, uri, file):
        Source.__init__(self)
        self.uri = uri
        self.file = file

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            plist = readPlist(self.file)

            for k, v in plist['SQLite']['servers'].items():
                connection = SQLiteConnection(self.uri, v['dbfilename'])
                self.connections.append(connection)

        return self.connections
