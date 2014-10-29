#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urlparse import urlparse
from plistlib import readPlist
from os.path import isfile

from ..sources import *
from .databaseconnection import *

class DBExplorerMySQLSource(Source):
    def __init__(self, file):
        Source.__init__(self)
        self.file = file
    def list(self):
        if not isfile(self.file):
            return self.connections
        if not self.connections:
            try:
                tree = ET.parse(self.file)
            except IOError, e:
                return []
            root = tree.getroot()
            for c in root.iter('connection'):
                url = urlparse(c.find('url').text.replace('jdbc:',''))
                if url.scheme == 'mysql':
                    host = url.netloc.split(':')[0]
                    port = 3306
                    database = '*'
                    user = c.find('user').text
                    password = c.find('password').text
                    connection = MySQLConnection(host, port, database, user, password)
                    self.connections.append(connection)
        
        return self.connections
