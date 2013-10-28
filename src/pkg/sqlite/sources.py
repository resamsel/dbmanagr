#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
from urlparse import urlparse

from ..sources import *
from .databaseconnection import *

class DBExplorerSQLiteSource(Source):
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
                if url.scheme == 'sqlite':
                    connection = SQLiteConnection(url.path)
                    self.connections.append(connection)
        
        return self.connections
