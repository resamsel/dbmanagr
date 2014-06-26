#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shelve
import logging
import time

from os.path import expanduser, basename

from ..logger import logduration
from ..model.databaseconnection import *
from ..model.database import *
from ..model.table import *
from ..model.column import *
from ..model.foreignkey import *
from ..options import *

CACHE_TIME = 2*60
COLUMNS_QUERY = """
pragma table_info({0})
"""

logger = logging.getLogger(__name__)

class SQLiteConnection(DatabaseConnection):
    """A database connection"""

    def __init__(self, path):
        logger.debug("SQLiteConnection.__init__(%s)", path)
        DatabaseConnection.__init__(self)
        self.path = path
        self.filename = basename(self.path)
        self.con = None
        self.dbs = None
        self.database = self.databases()[0]
        self.tbls = None
        self.driver = 'sqlite'

    def __repr__(self):
        return self.filename

    def autocomplete(self):
        return self.filename

    def title(self):
        return self.filename

    def subtitle(self):
        return 'SQLite Connection'

    def matches(self, options):
        options = options.get(self.driver)
        if options.uri:
            return options.uri.startswith(self.filename)
        return False

    def filter(self, options):
        options = options.get(self.driver)
        return not options.uri or options.uri in self.path

    def connect(self, database=None):
        logger.debug('Connecting to database %s' % database)
        
        self.connect_to('sqlite+pysqlite:///%s' % self.path)

    def databases(self):
        logger.debug('Retrieve databases')
        return [Database(self, '_')]

    def tablesof(self, database):
        def t(name): return Table(self, database, name, '')

        return map(t, [t for t in self.inspector.get_table_names()])
