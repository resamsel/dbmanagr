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

COLUMNS_QUERY = """
select
        column_name
    from
        information_schema.columns
    where
        table_name = '{0}'
"""

class Table:
    def __init__(self, connection, database, name, comment):
        self.database = database
        self.name = name
        self.comment = TableComment(self, comment)
        self.cols = None
        self.fks = {}
        self.uri = '%s@%s/%s' % (connection.user, connection.host, database)

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
        cur.execute(query)
        logduration('Query rows', start)

        def t(row): return Row(connection, self, row)

        return map(t, cur.fetchall())
    
    def columns(self, connection):
        """Retrieves the columns of the table"""

        if not self.cols:
            logging.debug('Retrieve columns')
            query = COLUMNS_QUERY.format(self.name)
            logging.debug('Query columns: %s' % query)
            cur = connection.cursor()
            start = time.time()
            cur.execute(query)
            logduration('Query columns', start)
            self.cols = []
            for row in cur.fetchall():
                self.cols.append(row['column_name'])

        return self.cols

