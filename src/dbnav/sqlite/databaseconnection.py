#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from os.path import basename

from dbnav.logger import LogWith
from dbnav.model.databaseconnection import DatabaseConnection
from dbnav.model.database import Database

COLUMNS_QUERY = """
pragma table_info({0})
"""
AUTOCOMPLETE_FORMAT = "%s/"

logger = logging.getLogger(__name__)


class SQLiteDatabase(Database):
    def __init__(self, filename):
        self.filename = filename

    def __repr__(self):
        return AUTOCOMPLETE_FORMAT % self.filename


class SQLiteConnection(DatabaseConnection):
    """A database connection"""

    def __init__(self, path):
        self.path = path
        self.filename = basename(self.path)
        self.con = None
        self.dbs = None
        DatabaseConnection.__init__(
            self,
            dbs='sqlite',
            database=self.databases()[0],
            driver='sqlite')

    def __repr__(self):
        return AUTOCOMPLETE_FORMAT % self.filename

    def autocomplete(self):
        return self.__repr__()

    def title(self):
        return self.__repr__()

    def subtitle(self):
        return 'SQLite Connection'

    def uri(self, table):
        return '%s%s' % (self.autocomplete(), table)

    def matches(self, options):
        options = options.get(self.dbs)
        if options.uri:
            return options.uri.startswith(self.filename)
        return False

    def filter(self, options):
        options = options.get(self.dbs)
        return not options.uri or options.uri in self.path

    @LogWith(logger)
    def connect(self, database=None):
        self.connect_to('sqlite+pysqlite:///%s' % self.path)

    def databases(self):
        return [SQLiteDatabase(self)]
