#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

import xml.etree.ElementTree as ET
from urlparse import urlparse
from plistlib import readPlist
from os.path import isfile

from dbnav.sources import Source
from .databaseconnection import SQLiteConnection

logger = logging.getLogger(__name__)


class DBExplorerSQLiteSource(Source):
    def __init__(self, file):
        logger.debug("DBExplorerSQLiteSource.__init__(%s)", file)
        Source.__init__(self)
        self.file = file

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            try:
                tree = ET.parse(self.file)
            except IOError:
                return []
            root = tree.getroot()
            for c in root.iter('connection'):
                url = urlparse(c.find('url').text.replace('jdbc:', ''))
                if url.scheme == 'sqlite':
                    logger.debug("Found connection: %s", url)
                    connection = SQLiteConnection(url.path)
                    self.connections.append(connection)

        return self.connections


class NavicatSQLiteSource(Source):
    def __init__(self, file):
        Source.__init__(self)
        self.file = file

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            plist = readPlist(self.file)

            for k, v in plist['SQLite']['servers'].items():
                connection = SQLiteConnection(v['dbfilename'])
                self.connections.append(connection)

        return self.connections
