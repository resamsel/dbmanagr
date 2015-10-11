# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

import logging

from collections import Counter
from sqlalchemy import or_, and_, String
from sqlalchemy.orm import aliased
from sqlalchemy.orm.session import Session

from dbmanagr.logger import LogWith
from dbmanagr.utils import create_title, operation
from dbmanagr.comment import create_comment
from dbmanagr.exception import UnknownColumnException
from dbmanagr.queryfilter import QueryFilter, OrOp, BitOp

logger = logging.getLogger(__name__)


def column_or_raise(table, columnname):
    column = table.column(columnname)
    if not column:
        raise UnknownColumnException(table, 'id')
    return column


@LogWith(logger)
def allowed(column, operator, value):
    if operator in ['~', '*']:
        return isinstance(column.type, String)
    if operator in ['=', '!=']:
        try:
            column.type.python_type(value)
            return True
        except BaseException:
            return False
    return True


def add_references(tablename, foreign_keys, joins, comment):
    for _, fk in filter(
            lambda (k, v): (
                v.a.table.name == tablename
                and (comment is None or k in comment.display)),
            foreign_keys.iteritems()):
        fktable = fk.b.table
        fkentity = fktable.entity()

        # Prevent multiple joins of the same table
        add_join(fkentity, joins)

    return joins


@LogWith(logger)
def add_join(entity, joins):
    if entity.name not in joins.keys():
        joins[entity.name] = aliased(
            entity, name='_{0}'.format(entity.name))

    return joins


def replace_filter(f, table, entity, comment, search_fields):
    if isinstance(f, BitOp):
        f.children = map(
            lambda child: replace_filter(
                child, table, entity, comment, search_fields),
            f.children)
    elif f.lhs == '' and search_fields:
        logger.debug('Search fields: %s', search_fields)
        rhs = f.rhs
        if rhs == '' and f.operator == '*':
            rhs = '%'
        ors = OrOp(map(
            lambda s: QueryFilter(s, f.operator, rhs),
            filter(
                lambda s: s in entity.columns,
                search_fields)))
        if 'id' in comment.columns:
            col = column_or_raise(table, 'id')
            ors.append(QueryFilter(col.name, f.operator, rhs))
        logger.debug('Searches: %s', ors)
        return ors
    return f


@LogWith(logger)
def add_filters(f, filters, table, joins):
    if isinstance(f, BitOp):
        op = {
            'OrOp': or_,
            'AndOp': and_
        }.get(f.__class__.__name__)
        fs = []

        for c in f.children:
            add_filters(c, fs, table, joins)

        logger.debug('Filter fs: %s', fs)

        if len(fs) > 1:
            filters.append(op(*fs))
        elif len(fs) > 0:
            filters.append(*fs)

    elif isinstance(f, QueryFilter):
        logger.debug(
            'Filter: lhs=%s, op=%s, rhs=%s',
            f.lhs, f.operator, f.rhs)
        if f.lhs != '':
            add_filter(f, filters, table, joins)


@LogWith(logger)
def add_filter(f, filters, table, joins):
    if not f.operator:
        return None

    if '.' in f.lhs:
        foreign_keys = table.foreign_keys()
        ref, colname = f.lhs.split('.', 1)
        if ref not in foreign_keys:
            raise UnknownColumnException(table, ref)
        t = foreign_keys[ref].b.table
        add_join(t.entity(), joins)
        return add_filter(
            QueryFilter(colname, f.operator, f.rhs), filters, t, joins)

    colname = f.lhs
    col = table.column(colname)
    if not col:
        raise UnknownColumnException(table, colname)
    tentity = joins[table.name]
    if allowed(tentity.columns[col.name], f.operator, f.rhs):
        op = operation(
            tentity.columns[col.name],
            f.operator,
            f.rhs)
        filters.append(op)
        return op
    else:
        filters.append(False)

    return None


def create_label(alias_format):
    return lambda column: column.label(alias_format.format(col=column))


def simplify(table, comment, key, d):
    if comment:
        d[key] = unicode(comment.__dict__[key]).format(table.name, **d)
        d['id'] = d[u'{0}_{1}'.format(
            comment.aliases[table.name], table.primary_key)]
    else:
        d[key] = create_title(
            comment, table.columns())[1].format(table.name, **d)


def with_filters(query, filters):
    """Adds filters"""

    for f in filters:
        query = query.filter(f)

    return query


def with_orders(query, orders):
    """Adds orders"""

    for order in orders:
        query = query.order_by(order)

    return query


class SimplifyMapper(object):
    def __init__(self, table, comment=None):
        self.table = table
        self.comment = comment

    def map(self, row):
        d = row.__dict__
        for k in filter(lambda k: k not in d, ['title', 'subtitle']):
            simplify(self.table, self.comment, k, d)
        return row


class QueryBuilder(object):
    def __init__(
            self,
            connection,
            table,
            filter_=None,
            order=None,
            limit=None,
            simplify=True):
        self.connection = connection
        self.table = table
        self.filter = filter_ if filter_ else OrOp()
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

        entity = aliased(self.table.entity(), name=self.alias)

        projection = map(lambda x: x, entity.columns)
        joins = {self.table.name: entity}

        if self.simplify:
            # Add referenced tables from comment to be linked
            comment = create_comment(
                self.table,
                self.connection.comment(self.table.name),
                self.counter,
                self.aliases,
                self.alias)

            add_references(self.table.name, foreign_keys, joins, comment)

            logger.debug('Joins: %s', joins)

            if not self.order:
                self.order = [self.table.primary_key]

            logger.debug('Order: %s', self.order)

            keys = dict(map(lambda k: (str(k), k), comment.columns.keys()))
            if comment.search:
                for s in comment.search:
                    search_fields.append(s.format(**keys))

            if not search_fields:
                search_fields.append(comment.title.format(**keys))

            logger.debug('Search fields: %s', search_fields)

            replace_filter(
                self.filter, self.table, entity, comment, search_fields)

        logger.debug('Aliases: %s', self.aliases)

        filters = []
        if self.filter:
            add_filters(self.filter, filters, self.table, joins)

        orders = []
        if self.order:
            for order in self.order:
                orders.append(entity.columns[order])

        # Create a session
        session = Session(self.connection.engine())

        # Create query
        if self.simplify:
            alias_format = '{col.table.name}_{col.name}'
        else:
            alias_format = '{col.name}'
        logger.debug('Projection: %s', projection)
        query = session.query(*map(create_label(alias_format), projection))
        logger.debug('Query (init): %s', query)

        # Add found joins
        # Aliased joins
        joins = dict(filter(
            lambda (k, v): k != entity.original.name,
            joins.iteritems()))
        logger.debug('Joins: %s', joins)
        for _, join in joins.iteritems():
            query = query.outerjoin(join)
            for column in join.columns.keys():
                col = join.columns[column]
                query = query.add_column(create_label(alias_format)(col))
        logger.debug('Query (joins): %s', query)

        query = with_filters(query, filters)
        query = with_orders(query, orders)

        logger.debug('Slice: 0, %d', self.limit)

        # For Markus: don't slice if limit is less than 1!
        if self.limit > 0:
            return query.slice(0, self.limit)

        return query
