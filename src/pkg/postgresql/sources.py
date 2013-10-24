#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import expanduser

import xml.etree.ElementTree as ET
from urlparse import urlparse

from ..sources import *
from .databaseconnection import *

class PgpassSource(Source):
    def list(self):
        if not self.connections:
            with open(expanduser('~/.pgpass')) as f:
                pgpass = f.readlines()

            for line in pgpass:
                connection = PostgreSQLConnection(*line.strip().split(':'))
                self.connections.append(connection)

        return self.connections

class DBExplorerSource(Source):
    def list(self):
        if not self.connections:
            try:
                tree = ET.parse(expanduser('~/.dbexplorer/dbexplorer.cfg'))
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