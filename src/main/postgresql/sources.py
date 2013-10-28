#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urlparse import urlparse

from ..sources import *
from .databaseconnection import *

class PgpassSource(Source):
    def __init__(self, file):
        Source.__init__(self)
        self.file = file
    def list(self):
        if not self.connections:
            with open(self.file) as f:
                pgpass = f.readlines()

            for line in pgpass:
                connection = PostgreSQLConnection(*line.strip().split(':'))
                self.connections.append(connection)

        return self.connections

class DBExplorerPostgreSQLSource(Source):
    def __init__(self, file):
        Source.__init__(self)
        self.file = file
    def list(self):
        if not self.connections:
            try:
                tree = ET.parse(self.file)
            except IOError, e:
                return []
            root = tree.getroot()
            for c in root.iter('connection'):
                url = urlparse(c.find('url').text.replace('jdbc:',''))
                if url.scheme == 'postgresql':
                    host = url.netloc
                    port = 5432
                    database = '*'
                    user = c.find('user').text
                    password = c.find('password').text
                    connection = PostgreSQLConnection(host, port, database, user, password)
                    self.connections.append(connection)
        
        return self.connections
