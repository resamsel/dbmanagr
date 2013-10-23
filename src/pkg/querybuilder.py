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
SEARCH_FORMAT = "%s like '%s%%'"
LIST_SEPARATOR = """,
        """
OR_SEPARATOR = """
        or """

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

        if not self.display:
            for column in table.columns(qb.connection):
                self.display.append(column)

        self.populate_titles(self.fk_titles, table.fks)

        def f(s):
            try:
                return s.format(self.alias, **self.fk_titles)
            except KeyError, e:
                logging.debug("Foreign key titles: %s" % self.fk_titles)
                logging.error("Error: %s" % e)
                return s
        
        self.id = f(comment.id)
        self.title = f(comment.title)
        self.subtitle = f(comment.subtitle)
        self.order = map(f, comment.order)
        self.search = map(f, comment.search)

        if 'id' in table.columns(qb.connection):
            self.columns['id'] = Projection(self.id, 'id')
        else:
            self.columns['id'] = Projection('1', 'id')
        if self.title != '*':
            self.columns['title'] = Projection(self.title, 'title')
        self.columns['subtitle'] = Projection(self.subtitle, 'subtitle')
        for column in self.display:
            self.columns[column] = Projection('%s.%s' % (self.alias, column), column)
        
        logging.debug('Columns: %s' % self.columns)

        if not self.search:
            self.search.append(self.title)
            self.search.append(self.subtitle)

    def populate_titles(self, fk_titles, foreign_keys):
        logging.debug("Populate titles: %s" % foreign_keys.keys())
        for key in foreign_keys.keys():
            if key in self.display:
                fk = foreign_keys[key]
                fktable = fk.b.table
                self.qb.counter[fktable.name] += 1
                alias = '%s_%d' % (fktable.name, self.qb.counter[fktable.name])
                self.qb.aliases[key] = alias
                k = '%s_title' % key
                try:
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

    def build(self):
        foreign_keys = self.table.fks
        where = 'true=true'
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
                        title = fktable.comment.title.format(alias)
                        if title != '*':
                            a = ALIAS_FORMAT.format(fk.a.name)
                            comment.columns[a] = Projection(title, a)
                        self.joins[alias] = Join(fk.b.table.name, alias, fk.b.name, self.alias, fk.a.name)
                    except KeyError, e:
                        logging.error("KeyError: %s, table=%s, comment.title=%s" % (e, fktable, fktable.comment.title))

        if self.id:
            if '=' in comment.id:
                (name, value) = comment.id.split('=')
                where = "{0}.{1} = '{2}'".format(self.alias, name, value)
            else:
                where = "%s = '%s'" % (comment.id, self.id)
        elif self.filter:
            if '=' in self.filter:
                (name, value) = self.filter.split('=')
                where = "{0}.{1} = '{2}'".format(self.alias, name, value)
            elif comment.search:
                conjunctions = []
                for search_field in comment.search:
                    conjunctions.append(SEARCH_FORMAT % (search_field, self.filter))
                if 'id' in comment.columns:
                    conjunctions.append("%s || '' = '%s'" % (comment.columns['id'].value, self.filter))
                where = OR_SEPARATOR.join(conjunctions)

        if not order:
            if 'id' in comment.columns:
                order.append(comment.columns['id'].value)
            else:
                order.append('1')

        return QUERY_FORMAT.format(self.table.name,
            LIST_SEPARATOR.join(map(str, comment.columns.values())),
            self.alias,
            ''.join(map(str, self.joins.values())),
            where,
            LIST_SEPARATOR.join(order),
            self.limit)
