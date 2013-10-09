#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from os.path import expanduser

import xml.etree.ElementTree as ET
from urlparse import urlparse

from model import *

class Source:
    def __init__(self):
        self.connections = []
    def get_connections(self):
        return self.connections

class PgpassSource(Source):
    def get_connections(self):
        if not self.connections:
            with open(expanduser('~/.pgpass')) as f:
                pgpass = f.readlines()

            for line in pgpass:
                connection = DatabaseConnection(*line.strip().split(':'))
                logging.debug('Database Connection: %s' % connection)
                self.connections.append(connection)

        return self.connections

class DBExplorerSource(Source):
    def get_connections(self):
        if not self.connections:
            tree = ET.parse(expanduser('~/.dbexplorer/dbexplorer.cfg'))
            root = tree.getroot()
            for c in root.iter('connection'):
                url = urlparse(c.find('url').text.replace('jdbc:',''))
                if url.scheme == 'postgresql':
                    host = url.netloc
                    port = 5432
                    database = url.path.split('/')[1]
                    user = c.find('user').text
                    password = c.find('password').text
                    connection = DatabaseConnection(host, port, database, user, password)
                    logging.debug('Database Connection: %s' % connection)
                    self.connections.append(connection)
        
        return self.connections