#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import text

from dbnav.logger import logger
from dbnav.comment import Comment

OPERATORS = {
    '=':    lambda q, c, v: q.filter(c == v),
    '!=':   lambda q, c, v: q.filter(c != v),
    '~':    lambda q, c, v: q.filter(c.like(v)),
    '*':    lambda q, c, v: q.filter(c.like(v)),
    '>':    lambda q, c, v: q.filter(c > v),
    '>=':   lambda q, c, v: q.filter(c >= v),
    '<=':   lambda q, c, v: q.filter(c <= v),
    '<':    lambda q, c, v: q.filter(c < v),
    'in':   lambda q, c, v: q.filter(c.in_(v)),
    ':':    lambda q, c, v: q.filter(c.in_(v))
}

def add_filter(query, column, operator, value):
    return OPERATORS.get(operator)(query, column, value)

class SimplifyMapper:
    def __init__(self, table, comment=None):
        self.table = table
        self.comment = comment
    def map(self, row):
        d = row.__dict__
        print d.keys()
        if 'title' not in d:
            if self.comment:
                d['title'] = self.comment.title
            elif self.table.primary_key:
                d['title'] = d[self.table.primary_key]
            else:
                d['title'] = row[0]
        if 'subtitle' not in d:
            if self.comment:
                d['subtitle'] = self.comment.subtitle
            else:
                d['subtitle'] = ''

class QueryBuilder:
    def __init__(self, connection, table, id=None, filter=None, order=None, limit=None, simplify=True):
        self.connection = connection
        self.table = table
        self.id = id
        self.filter = filter if filter else []
        self.order = order if order else []
        self.limit = limit
        self.aliases = {}
        self.joins = {}
        self.counter = Counter()
        self.simplify = simplify

        self.alias = '_%s' % self.table.name

    def build(self):
        foreign_keys = self.table.foreign_keys()

        Entity = self.table.table

        session = Session(self.connection.engine)
        query = session.query(Entity).enable_eagerloads(True)

        if self.simplify:
            # Add referenced tables from comment to be linked
            comment = Comment(self.table, self.counter, self.aliases, self.alias)

            for key in foreign_keys.keys():
                if key in comment.display:
                    fk = foreign_keys[key]
                    fktable = fk.b.table
                    logger.debug('Adding join for table %s', fktable.name)
                    query = query.join(fktable.table)

        if self.filter:
            wheres = []
            for f in self.filter:
                logger.debug("Filter: column=%s, operator=%s, filter=%s",
                     f.lhs, f.operator, f.rhs)
                if f.lhs != '':
                    if f.operator:
                        logger.debug('lhs=%s, operator=%s, rhs=%s',
                            f.lhs, f.operator, f.rhs)
                        col = self.table.column(f.lhs)
                        if not col:
                            raise UnknownColumnException(self.table, f.lhs)
                        query = add_filter(query,
                            Entity.columns[col.name],
                            f.operator,
                            f.rhs)

        return query.slice(0, self.limit)
