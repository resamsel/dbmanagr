#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from collections import Counter

QUERY_FORMAT = """
select
        {1}
    from
        "{0}" {2}{3}
    where
        {4}
    order by
        {5}
    limit
        {6}
"""
JOIN_FORMAT = """
        left outer join \"{0}\" {1} on {1}.{2} = {3}.{4}"""
ALIAS_FORMAT = "{0}_title"
PROJECTION_FORMAT = """{0} {1}"""
SEARCH_FORMAT = "cast(%s as text) %s '%s'"
LIST_SEPARATOR = """,
        """
OR_SEPARATOR = """
        or """

logger = logging.getLogger(__name__)

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
        if not comment.title:
            if comment.id:
                comment.title = comment.id
            else:
                comment.title = '{0}.%s' % columns[0].name
        if not comment.subtitle:
            if table.primary_key:
                comment.subtitle = "'Primary key is %s'" % table.primary_key
            else:
                comment.subtitle = "'There is no primary key'"
        if not comment.id:
            comment.id = "'-'"

        if not self.display:
            for column in columns:
                self.display.append(column.name)

        self.populate_titles(self.fk_titles, table.fks)

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
    def __init__(self, connection, table, id=None, filter=None, order=[], limit=None):
        self.connection = connection
        self.table = table
        self.id = id
        self.filter = filter
        self.order = order
        self.limit = limit
        self.aliases = {}
        self.joins = {}
        self.counter = Counter()

        self.alias = '_%s' % self.table.name
        logger.debug("QueryBuilder: order=%s, self=%s", order, self.__dict__)

    def build(self):
        logger.debug("QueryBuilder: %s", self.__dict__)
        foreign_keys = self.table.foreign_keys()
        where = '1=1'
        order = self.order
        limit = self.limit if self.limit else 20
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
            logger.debug("Filter: column=%s, operator=%s, filter=%s",
                 self.filter.column, self.filter.operator, self.filter.filter)
            operator = {
                '=': '=',
                '~': 'like',
                '*': 'like'
            }.get(self.filter.operator, '=')
            if self.filter.column != '' and self.filter.column in comment.columns:
                if self.filter.operator:
                    name = self.filter.column
                    value = self.filter.filter.replace('%', '%%')
                    where = "{0}.{1} {2} '{3}'".format(self.alias, name, operator, value)
            elif comment.search:
                f = self.filter.filter.replace('%', '%%')
                if f == '' and self.filter.operator == '*':
                    f = '%%'
                conjunctions = []
                for search_field in comment.search:
                    conjunctions.append(SEARCH_FORMAT % (search_field, operator, f))
                if 'id' in comment.columns:
                    conjunctions.append(SEARCH_FORMAT % (comment.columns['id'].value, operator, f))
                where = OR_SEPARATOR.join(conjunctions)

        logger.debug('Order before: %s', order)

        if not order:
            if 'id' in comment.columns:
                order.append(comment.columns['id'].value)
            else:
                order.append('1')
        
        logger.debug('Order after: %s', order)

        return QUERY_FORMAT.format(self.table.name,
            LIST_SEPARATOR.join(map(str, comment.columns.values())),
            self.alias,
            ''.join(map(str, self.joins.values())),
            where,
            LIST_SEPARATOR.join(order),
            self.limit)
