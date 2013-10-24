#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from ..logger import logduration
from .tablecomment import TableComment
from .row import Row
from ..querybuilder import QueryBuilder

DEFAULT_LIMIT = 50

OPTION_URI_VALUE_FORMAT = '%s/%s/%s/'

class Table:
    def __init__(self, connection, database, name, comment):
        self.database = database
        self.name = name
        self.comment = TableComment(self, comment)
        self.cols = None
        self.fks = {}
        self.uri = str(connection)
        if self.uri.endswith('/'):
            self.uri += database
        self.primary_key = 'id'

    def __repr__(self):
        return self.name

    def autocomplete(self, column, value, format=OPTION_URI_VALUE_FORMAT):
        """Retrieves the autocomplete string for the given column and value"""

        tablename = self.name
        fks = self.fks
        if column in fks:
            fk = fks[column]
            tablename = fk.b.table.name

        return format % (self.uri, tablename, value)

    def rows(self, connection, filter):
        """Retrieves rows from the table with the given filter applied"""

        query = QueryBuilder(connection, self, filter=filter, order=self.comment.order, limit=DEFAULT_LIMIT).build()

        logging.debug('Query rows: %s' % query)
        cur = connection.cursor()
        start = time.time()
        try:
            cur.execute(query)
        except BaseException, e:
            logging.error('%s: check comment on table %s\n%s' % (e.__class__.__name__, self.name, str(e)))
            from ..model import databaseconnection
            return [Row(connection, self, databaseconnection.Row({'title': str(e), 'subtitle': 'Check comment on table %s' % self.name}))]
        logduration('Query rows', start)

        def t(row): return Row(connection, self, row)

        return map(t, cur.fetchall())
    
    def foreign_keys(self):
        return self.fks