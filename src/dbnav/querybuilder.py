#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from collections import Counter
from sqlalchemy import or_, String
from sqlalchemy.orm import aliased
from sqlalchemy.orm.session import Session

from dbnav.logger import LogWith
from dbnav.utils import create_title
from dbnav.comment import create_comment
from dbnav.model.exception import UnknownColumnException

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


logger = logging.getLogger(__name__)


@LogWith(logger)
def allowed(column, operator, value):
    if operator in ['~', '*']:
        return isinstance(column.type, String)
    return True


def operation(column, operator, value):
    return OPERATORS.get(operator)(column, value)


def add_references(display, foreign_keys, projection, joins):
    for key in foreign_keys.keys():
        fk = foreign_keys[key]
        fktable = fk.b.table
        prefix = '%s.' % key
        for column in map(
                lambda c: c.replace(prefix, ''),
                filter(
                    lambda d: d.startswith(prefix),
                    display)):
            logger.debug('Adding join for %s', fk.b.name)
            fkentity = fktable.entity
            projection.append(fkentity.columns[column])

            # Prevent multiple joins of the same table
            if fkentity not in joins:
                joins.append(fkentity)


class SimplifyMapper:
    def __init__(self, table, comment=None):
        self.table = table
        self.comment = comment

    @LogWith(logger)
    def map(self, row):
        d = row.__dict__
        for k in filter(
                lambda k: k not in d,
                ['title', 'subtitle']):
            if self.comment:
                logger.debug(
                    'Formatting %s: "%s".format(%s, **%s)',
                    k, self.comment.__dict__[k], self.table.name, d)
                d[k] = self.comment.__dict__[k].format(
                    self.table.name, **d)
            else:
                d[k] = create_title(
                    self.comment, self.table.columns()).format(
                        self.table.name, **d)[1]


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
        self.counter = Counter()
        self.simplify = simplify

        self.alias = '_%s' % self.table.name

    @LogWith(logger)
    def build(self):
        foreign_keys = self.table.foreign_keys()
        search_fields = []

        entity = aliased(self.table.entity, name=self.alias)

        projection = map(lambda x: x, entity.columns)
        joins = []
        if self.simplify:
            # Add referenced tables from comment to be linked
            comment = create_comment(
                self.table,
                self.connection.comment(self.table.name),
                self.counter,
                self.aliases,
                self.alias)

            logger.debug(
                'Comment: %s, foreign keys: %s',
                comment, foreign_keys.keys())

            add_references(comment.display, foreign_keys, projection, joins)

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

        logger.debug('Aliases: %s', self.aliases)

        filters = []
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
                        if allowed(
                                entity.columns[col.name], f.operator, f.rhs):
                            filters.append(
                                operation(
                                    entity.columns[col.name],
                                    f.operator,
                                    f.rhs))
                elif search_fields:
                    logger.debug('Search fields: %s', search_fields)
                    rhs = f.rhs
                    if rhs == '' and f.operator == '*':
                        rhs = '%'
                    ss = map(
                        lambda s: operation(
                            entity.columns[s], f.operator, rhs),
                        filter(
                            lambda s: s in entity.columns and allowed(
                                entity.columns[s], f.operator, rhs),
                            search_fields))
                    if 'id' in comment.columns:
                        col = self.table.column('id')
                        if not col:
                            raise UnknownColumnException(self.table, 'id')
                        column = entity.columns[col.name]
                        if allowed(column, f.operator, rhs):
                            ss.append(operation(column, f.operator, rhs))
                    filters.append(or_(*ss))

        orders = []
        if self.order:
            for order in self.order:
                orders.append(entity.columns[order])

        # Create a session
        session = Session(self.connection.engine)

        # Create query
        logger.debug('Projection: %s', projection)
        query = session.query(*projection)

        # Add found joins
        for join in joins:
            query = query.join(join)

        # Add filters
        for f in filters:
            query = query.filter(f)

        # Add orders
        for order in orders:
            query = query.order_by(order)

        logger.debug('Slice: 0, %d', self.limit)

        # For Markus: don't slice if limit is less than 1!
        if self.limit > 0:
            return query.slice(0, self.limit)

        return query
