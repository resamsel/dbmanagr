#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import time

from ..model.databaseconnection import *
from ..model.database import *
from ..model.table import *
from ..model.column import *
from ..model.foreignkey import *

class MockConnection(DatabaseConnection):
    """A database connection"""

    def __init__(self, host, port, database, user, password):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        
        self.dbs = [Database(self, 'mockdb')]
        self.tbls = {t.name: t for t in [Table(self, self.dbs[0], 'mocktable', '')]}

    def __repr__(self):
        return '%s@%s/%s' % (self.user, self.host, self.database if self.database != '*' else '')

    def title(self):
        return self.autocomplete()

    def subtitle(self):
        return 'Mock Connection'
    
    def autocomplete(self):
        return self.__repr__()
    
    def matches(self, s):
        return s.startswith("%s@%s" % (self.user, self.host))

    def databases(self):
        return self.dbs

    def tables(self):
        return self.tbls
