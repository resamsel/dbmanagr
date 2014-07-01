#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from ..logger import logduration
from .tablecomment import TableComment
from .column import *
from .row import *
from ..querybuilder import QueryBuilder

DEFAULT_LIMIT = 50

OPTION_URI_VALUE_FORMAT = '%s%s/%s/'

logger = logging.getLogger(__name__)

class Table:
    def __init__(self, connection, database, name, comment):
        self.database = database
        self.name = name
        self.comment = TableComment(self, comment)
        self.cols = None
        self.fks = {}
        self.uri = connection.autocomplete()
        self.primary_key = 'id'

    def __repr__(self):
        return self.name

    def autocomplete(self, column=None, value=None, format=OPTION_URI_VALUE_FORMAT):
        """Retrieves the autocomplete string for the given column and value"""

        logger.debug('autocomplete(self=%s, column=%s, value=%s, format=%s)', self, column, value, format)

        if column == None:
            return '%s%s/' % (self.uri, self.name)

        tablename = self.name
        fks = self.fks
        value = '%s=%s' % (column, value)

        return format % (self.uri, tablename, value)

    def columns(self, connection, column):
        """Retrieves columns of table with given filter applied"""
        
        cols = connection.inspector.get_columns(self.name)
        
        return [Column(self, c['name']) for c in cols if column in c['name']]

    def rows(self, connection, filter):
        """Retrieves rows from the table with the given filter applied"""

        query = QueryBuilder(connection,
            self,
            filter=filter,
            order=self.comment.order,
            limit=DEFAULT_LIMIT).build()

        try:
            result = connection.execute(query, 'Rows')
        except BaseException, e:
            logger.error(
                '%s: check comment on table %s\n%s' % (
                    e.__class__.__name__,
                    self.name,
                    str(e)))
            from ..model import databaseconnection
            return [Row(connection,
                self,
                databaseconnection.Row({'title': str(e), 'subtitle': 'Check comment on table %s' % self.name}))]

        def t(row): return Row(connection, self, row)

        return map(t, result)
    
    def foreign_keys(self):
        return self.fks
