#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os.path import expanduser

import xml.etree.ElementTree as ET
from urlparse import urlparse

from ..sources import *
from .databaseconnection import *

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
                if url.scheme == 'sqlite':
                    connection = SQLiteConnection(url.path)
                    self.connections.append(connection)
        
        return self.connections
