#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urlparse import urlparse
from os.path import isfile

from dbnav.sources import Source
from .databaseconnection import MySQLConnection


class MypassSource(Source):
    def __init__(self, driver, file):
        Source.__init__(self)
        self.driver = driver
        self.file = file

    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            with open(self.file) as f:
                mypass = f.readlines()

            for line in mypass:
                connection = MySQLConnection(
                    self.driver, *line.strip().split(':'))
                self.connections.append(connection)

        return self.connections


class DBExplorerMySQLSource(Source):
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
                if url.scheme == 'mysql':
                    host = url.netloc.split(':')[0]
                    port = 3306
                    database = '*'
                    user = c.find('user').text
                    password = c.find('password').text
                    connection = MySQLConnection(
                        self.driver, host, port, database, user, password)
                    self.connections.append(connection)

        return self.connections
