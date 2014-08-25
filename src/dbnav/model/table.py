#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging

from ..logger import logduration
from .tablecomment import TableComment
from .column import *
from .row import *
from ..querybuilder import QueryBuilder
from .baseitem import BaseItem

DEFAULT_LIMIT = 50

OPTION_URI_VALUE_FORMAT = '%s%s/%s/'

logger = logging.getLogger(__name__)

class Table(BaseItem):
    def __init__(self, connection, database, name, comment, owner=None, size=None):
        self.connection = connection
        self.database = database
        self.name = name
        self.comment = TableComment(self, comment)
        self.owner = owner
        self.size = size
        self.cols = None
        self.fks = {}
        self.uri = connection.autocomplete()
        self.primary_key = 'id'

    def __repr__(self):
        return self.name

    def autocomplete(self, column=None, value=None, format=OPTION_URI_VALUE_FORMAT):
        """Retrieves the autocomplete string for the given column and value"""

        if column == None:
            return u'%s%s/' % (self.uri, self.name)

        tablename = self.name
        fks = self.fks
        if type(value) is buffer:
            value = '[BLOB]'
        else:
            value = u'%s=%s' % (column, value)

        return format % (self.uri, tablename, value)

    def init_columns(self, connection):
        self.cols = connection.columns(self)

    def columns(self, connection, column):
        """Retrieves columns of table with given filter applied"""
        
        if not self.cols:
            self.init_columns(connection)
        
        return [c for c in self.cols if column in c.name]

    def column(self, name):
        if not self.cols:
            self.init_columns(self.connection)
        
        for col in self.cols:
            if col.name == name:
                return col

        return None

    def rows(self, filter=[], limit=DEFAULT_LIMIT, artificial_projection=False):
        """Retrieves rows from the table with the given filter applied"""
        
        query = QueryBuilder(self.connection,
            self,
            filter=filter,
            order=self.comment.order,
            limit=limit,
            artificial_projection=artificial_projection).build()

        try:
            result = self.connection.execute(query, 'Rows')
        except BaseException, e:
            logger.error(
                '%s: check comment on table %s\n%s' % (
                    e.__class__.__name__,
                    self.name,
                    str(e)))
            logger.error(e, exc_info=1)
            from ..model import databaseconnection
            return [Row(self.connection,
                self,
                databaseconnection.DatabaseRow({'title': str(e), 'subtitle': 'Check comment on table %s' % self.name}))]

        def t(row): return Row(self.connection, self, row)

        return map(t, result)
    
    def foreign_keys(self):
        return self.fks

    def foreign_key(self, name):
        if name in self.fks:
            return self.fks[name]
        return None

    def title(self):
        return self.name

    def subtitle(self):
        if self.owner and self.size:
            return u'Owner: %s (%s)' % (self.owner, self.size)
        return u'Table'

    def icon(self):
        return 'images/table.png'
    
    def escaped(self, f):
        return dict(map(lambda (k, v): (k.encode('ascii', 'ignore'), f(v)), self.__dict__.iteritems()))
    
