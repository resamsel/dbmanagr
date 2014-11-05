#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import Counter
from sqlalchemy import or_, Integer
from sqlalchemy.orm.session import Session

from dbnav.logger import logger
from dbnav.comment import Comment
from dbnav.model.exception import UnknownColumnException

NAMES = [
    'name', 'title', 'key', 'text', 'username', 'user_name', 'email', 'comment'
]
OPERATORS = {
    '=': lambda c, v: c == v,
    '!=': lambda c, v: c != v,
    '~': lambda c, v: c.like(v),
    '*': lambda c, v: c.like(v),
    '>': lambda c, v: c > v,
    '>=': lambda c, v: c >= v,
    '<=': lambda c, v: c <= v,
    '<': lambda c, v: c < v,
    'in': lambda c, v: c.in_(v),
    ':': lambda c, v: c.in_(v)
}


def add_filter(query, column, operator, value):
    return query.filter(OPERATORS.get(operator)(column, value))


def create_title(comment, columns):
    logger.debug('create_title(comment=%s, columns=%s)', comment, columns)

    # find specially named columns (but is not an integer - integers are no
    # good names)
    for c in filter(lambda c: not isinstance(c.type, Integer), columns):
        for name in NAMES:
            logger.debug('c.name=%s, name=%s', c.name, name)
            if c.name == name:
                return c.name

    # find columns that end with special names
    for c in filter(lambda c: not isinstance(c.type, Integer), columns):
        for name in ['name', 'title', 'key', 'text']:
            logger.debug('c.name=%s, name=%s', c.name, name)
            if c.name.endswith(name):
                return c.name

    if comment.id:
        return comment.id

    return columns[0].name


class SimplifyMapper:
    def __init__(self, table, comment=None):
        self.table = table
        self.comment = comment

    def map(self, row):
        d = row.__dict__
        for k in ['title', 'subtitle']:
            if k not in d:
                if self.comment:
                    d[k] = self.comment.__dict__[k].format(
                        self.table.name, **d)
                else:
                    d[k] = create_title(
                        self.comment, self.table.columns()).format(
                            self.table.name, **d)


class QueryBuilder:
    def __init__(
            self,
            connection,
            table,
            filter=None,
            order=None,
            limit=None,
            simplify=True):
        self.connection = connection
        self.table = table
        self.filter = filter if filter else []
        self.order = order if order else []
        self.limit = limit
        self.aliases = {}
        self.joins = {}
        self.counter = Counter()
        self.simplify = simplify

        self.alias = '_%s' % self.table.name

    def build(self):
        logger.debug('QueryBuilder.build(self)')

        foreign_keys = self.table.foreign_keys()
        search_fields = []

        Entity = self.table.entity

        session = Session(self.connection.engine)
        query = session.query(Entity).enable_eagerloads(True)

        if self.simplify:
            logger.debug('Simplify result')

            # Add referenced tables from comment to be linked
            comment = Comment(
                self.table, self.counter, self.aliases, self.alias)

            logger.debug('Comment: %s', comment)

            for key in foreign_keys.keys():
                if key in comment.display:
                    fk = foreign_keys[key]
                    fktable = fk.b.table
                    logger.debug('Adding join for table %s', fktable.name)
                    query = query.join(fktable.entity)

            if not self.order:
                if 'id' in comment.columns:
                    self.order = [comment.columns['id']]

            logger.debug('Order: %s', self.order)

            keys = dict(map(lambda k: (str(k), k), comment.columns.keys()))
            if comment.search:
                for s in comment.search:
                    search_fields.append(s.format(**keys))

            if not search_fields:
                search_fields.append(comment.title.format(**keys))

            logger.debug('Search fields: %s', search_fields)

        if self.filter:
            for f in self.filter:
                logger.debug(
                    'Filter: lhs=%s, op=%s, rhs=%s',
                    f.lhs, f.operator, f.rhs)
                if f.lhs != '':
                    if f.operator:
                        logger.debug(
                            'lhs=%s, operator=%s, rhs=%s',
                            f.lhs, f.operator, f.rhs)
                        col = self.table.column(f.lhs)
                        if not col:
                            raise UnknownColumnException(self.table, f.lhs)
                        logger.debug(
                            'Adding filter: lhs=%s, operator=%s, rhs=%s',
                            f.lhs, f.operator, f.rhs)
                        query = add_filter(
                            query,
                            Entity.columns[col.name],
                            f.operator,
                            f.rhs)
                elif search_fields:
                    logger.debug('Search fields: %s', search_fields)
                    rhs = f.rhs
                    if rhs == '' and f.operator == '*':
                        rhs = '%'
                    ss = map(
                        lambda s: OPERATORS.get(f.operator)(
                            Entity.columns[s], rhs),
                        filter(
                            lambda s: s in Entity.columns,
                            search_fields))
                    if 'id' in comment.columns:
                        col = self.table.column('id')
                        if not col:
                            raise UnknownColumnException(self.table, 'id')
                        ss.append(OPERATORS.get(f.operator)(
                            Entity.columns[col.name], rhs))
                    query = query.filter(or_(*ss))

        if self.order:
            for order in self.order:
                query = query.order_by(Entity.columns[order])

        logger.debug('Slice: 0, %d', self.limit)

        return query.slice(0, self.limit)
