#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urlparse import urlparse
from plistlib import readPlist
from os.path import isfile

from dbnav.sources import Source
from .databaseconnection import PostgreSQLConnection


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
            except IOError:
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
    def __init__(self, file):
        Source.__init__(self)
        self.file = file

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            plist = readPlist(self.file)

            for k, v in plist['PostgreSQL']['servers'].items():
                # The key is a big problem here: it is encrypted
                connection = PostgreSQLConnection(
                    v['host'], v['port'],
                    v['defaultdatabase'], v['username'], v['key'])
                self.connections.append(connection)

        return self.connections
