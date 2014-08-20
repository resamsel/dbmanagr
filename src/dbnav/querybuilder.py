#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from collections import Counter
from sqlalchemy.types import Integer
from .model.column import Column

QUERY_FORMAT = """
select
        {1}
    from
        "{0}" {2}{3}
    where
        {4}
    order by
        {5}
    {6}
"""
LIMIT_FORMAT = "limit {0}"
JOIN_FORMAT = """
        left outer join \"{0}\" {1} on {1}.{2} = {3}.{4}"""
ALIAS_FORMAT = "{0}_title"
PROJECTION_FORMAT = """{0} {1}"""
SEARCH_FORMAT = "cast(%s as text) %s '%s'"
LIST_SEPARATOR = """,
        """
AND_SEPARATOR = """
        and """
OR_SEPARATOR = """
        or """
OPERATORS = {
    '=': '=',
    '~': 'like',
    '*': 'like',
    '>': '>',
    '>=': '>=',
    '<=': '<=',
    '<': '<',
    'in': 'in'
}

logger = logging.getLogger(__name__)

class QueryFilter:
    def __init__(self, lhs, operator=None, rhs=None):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs
class Join:
    def __init__(self, table, alias, column, fk_alias, fk_column):
        self.table = table
        self.alias = alias
        self.column = column
        self.fk_alias = fk_alias
        self.fk_column = fk_column
    def __repr__(self):
        return JOIN_FORMAT.format(self.table, self.alias, self.column, self.fk_alias, self.fk_column)
    def __str__(self):
        return self.__repr__()
class Projection:
    def __init__(self, value, alias):
        self.value = value
        self.alias = None

        if not value.endswith('.%s' % alias):
            self.alias = alias
    def __repr__(self):
        if not self.alias:
            return self.value
        return PROJECTION_FORMAT.format(self.value, self.alias)
    def __str__(self):
        return self.__repr__()
class Comment:
    def __init__(self, qb, table):
        self.qb = qb
        self.alias = qb.alias

        comment = table.comment

        self.fk_titles = {}
        self.columns = {}
        self.display = comment.display
        table.primary_key = None

        columns = qb.connection.columns(table)
        
        # finds the primary key
        for c in columns:
            if c.primary_key:
                table.primary_key = c.name
                break
        logger.debug("Primary key of table %s: %s", table.name, table.primary_key)

        if not comment.id and table.primary_key:
            comment.id = '{0}.%s' % table.primary_key
        if not comment.id:
            comment.id = "'-'"

        if not self.display:
            for column in columns:
                self.display.append(column.name)

        self.populate_titles(self.fk_titles, table.fks)

        if not comment.title:
            name, title = self.create_title(comment, columns)
            comment.title = title
            if name == table.primary_key:
                comment.subtitle = "'%s'" % name
            else:
                comment.subtitle = "'%s (id=' || %s || ')'" % (name, comment.id)
        if not comment.subtitle:
            if table.primary_key:
                comment.subtitle = "'%s'" % table.primary_key
            else:
                comment.subtitle = "'There is no primary key'"

        def f(s):
            try:
                return s.format(self.alias, **self.fk_titles)
            except KeyError, e:
                logger.debug("Foreign key titles: %s" % self.fk_titles)
                logger.error("Error: %s" % e)
                return s
        
        self.id = f(comment.id)
        self.title = f(comment.title)
        self.subtitle = f(comment.subtitle)
        self.order = map(f, comment.order)
        self.search = map(f, comment.search)

        if table.primary_key in [c.name for c in columns]:
            self.columns[table.primary_key] = Projection(self.id, 'id')
        else:
            self.columns[table.primary_key] = Projection("'-'", 'id')
        if self.title != '*':
            self.columns['title'] = Projection(self.title, 'title')
        self.columns['subtitle'] = Projection(self.subtitle, 'subtitle')
        for column in self.display:
            self.columns[column] = Projection('%s.%s' % (self.alias, column), column)
        
        if not self.search:
            self.search.append(self.title)
            self.search.append(self.subtitle)

    def __repr__(self):
        return str(self.__dict__)

    def create_title(self, comment, columns):
        logger.debug('create_title(comment=%s, columns=%s)', comment, columns)

        # find specially named columns (but is not an integer - integers are no good names)
        for c in columns:
            logger.debug('Column %s', c.name)
            for name in ['name', 'title', 'key', 'text', 'username', 'user_name', 'email', 'comment']:
                if c.name == name:
                    if not isinstance(c.type, Integer):
                        return (name, '{0}.%s' % c.name)
                    elif self.fk_titles['%s_title' % name]:
                        return ('%s_title' % name, self.fk_titles['%s_title' % name])

        # find columns that end with special names
        for c in columns:
            for name in ['name', 'title', 'key', 'text']:
                if c.name.endswith(name) and not isinstance(c.type, Integer):
                    return (name, '{0}.%s' % c.name)

        if comment.id:
            return ('id', comment.id)

        return ('First column', '{0}.%s' % columns[0].name)

    def populate_titles(self, fk_titles, foreign_keys):
        #logger.debug("Populate titles: %s", foreign_keys.keys())
        for key in foreign_keys.keys():
            if key in self.display:
                fk = foreign_keys[key]
                fktable = fk.b.table
                self.qb.counter[fktable.name] += 1
                alias = '%s_%d' % (fktable.name, self.qb.counter[fktable.name])
                self.qb.aliases[key] = alias
                k = '%s_title' % key
                try:
                    if fktable.comment.title:
                        fk_titles[k] = fktable.comment.title.format(alias)
                except KeyError, e:
#                    c = Comment(self.qb, fktable)
#                    columns = c.columns
#                    k_ = k.replace('%s_' % fk.a.name, '')
                    fk_titles[k] = "'columns[k_]'"
#                    self.qb.joins[fktable.name] = Join(fktable.name, alias, fk.b.name, self.alias, fk.a.name)
        
class QueryBuilder:
    def __init__(self, connection, table, id=None, filter=[], order=[], limit=None, artificial_projection=True):
        self.connection = connection
        self.table = table
        self.id = id
        self.filter = filter
        self.order = order
        self.limit = limit
        self.aliases = {}
        self.joins = {}
        self.counter = Counter()
        self.artificial_projection = artificial_projection

        self.alias = '_%s' % self.table.name
        logger.debug("QueryBuilder: order=%s, self=%s", order, self.__dict__)

    def build(self):
        logger.debug("QueryBuilder: %s", self.__dict__)
        foreign_keys = self.table.foreign_keys()
        where = '1=1'
        order = self.order
        limit = LIMIT_FORMAT.format(self.limit) if self.limit > 0 else ''
        comment = Comment(self, self.table)
        
        for key in foreign_keys.keys():
            if key in comment.display:
                fk = foreign_keys[key]
                fktable = fk.b.table
                if key in self.aliases:
                    alias = self.aliases[key]
                    try:
                        if fktable.comment.title:
                            title = fktable.comment.title.format(alias)
                            if title != '*':
                                a = ALIAS_FORMAT.format(fk.a.name)
                                comment.columns[a] = Projection(title, a)
                        self.joins[alias] = Join(fk.b.table.name, alias, fk.b.name, self.alias, fk.a.name)
                    except KeyError, e:
                        logger.error("KeyError: %s, table=%s, comment.title=%s" % (e, fktable, fktable.comment.title))

        logger.debug('Comment for %s: %s', self.table, comment)

        if self.id:
            if '=' in comment.id:
                (name, value) = comment.id.split('=')
                where = "{0}.{1} = '{2}'".format(self.alias, name, value)
            else:
                where = "%s = '%s'" % (comment.id, self.id)
        elif self.filter:
            wheres = []
            for f in self.filter:
                logger.debug("Filter: column=%s, operator=%s, filter=%s",
                     f.lhs, f.operator, f.rhs)
                operator = OPERATORS.get(f.operator, '=')
                if f.lhs != '':
                    if f.operator:
                        logger.debug('lhs=%s, operator=%s, rhs=%s', f.lhs, f.operator, f.rhs)
                        wheres.append(self.connection.restriction(
                            self.alias,
                            self.table.column(f.lhs),
                            operator,
                            f.rhs))
                elif comment.search:
                    rhs = f.rhs
                    if rhs == '' and f.operator == '*':
                        rhs = '%'
                    conjunctions = []
                    for search_field in comment.search:
                        def col(alias, field):
                            prefix = '%s.' % alias
                            if field.startswith(prefix):
                                field = field[len(prefix):]
                            c = self.table.column(field)
                            if c:
                                return c
                            return Column(None, field, False, 'String')
                        logger.debug('Search field: %s', search_field)
                        conjunctions.append(self.connection.restriction(
                            self.alias,
                            col(self.alias, search_field),
                            operator,
                            rhs))
                    if 'id' in comment.columns:
                        conjunctions.append(self.connection.restriction(
                            self.alias,
                            self.table.column('id'),
                            operator,
                            rhs))
                    wheres.append(OR_SEPARATOR.join(conjunctions))
            if wheres:
                where = AND_SEPARATOR.join(wheres)

        logger.debug('Order before: %s', order)

        if not order:
            if 'id' in comment.columns:
                order.append(comment.columns['id'].value)
            else:
                order.append('1')
        
        logger.debug('Order after: %s', order)
        
        if self.artificial_projection:
            projection = comment.columns.values()
        else:
            projection = [Projection('%s.%s' % (self.alias, col.name), col.name) for col in self.table.cols]

        return QUERY_FORMAT.format(self.table.name,
            LIST_SEPARATOR.join(map(str, projection)),
            self.alias,
            ''.join(map(str, self.joins.values())),
            where,
            LIST_SEPARATOR.join(order),
            limit)
