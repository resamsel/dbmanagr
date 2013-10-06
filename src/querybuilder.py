#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import logging
from collections import Counter

from const import *

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
PROJECTION_FORMAT = """{0} {1}_title"""
LIST_SEPARATOR = """,
        """
OR_SEPARATOR = """
        or """

class QueryBuilder:
    def __init__(self, table, id=None, filter=None, order=[], limit=None):
        self.table = table
        self.id = id
        self.filter = filter
        self.order = order
        self.limit = limit

        self.alias = '_%s' % self.table.name

    def build(self):
        foreign_keys = self.table.foreign_keys()
        columns = []
        joins = ''
        counter = Counter()
        aliases = {}
        fk_titles = {}
        where = 'true=true'
        order = self.order
        limit = self.limit if self.limit else 20
        comment_display = self.table.comment[COMMENT_DISPLAY]

        for key in foreign_keys.keys():
            if key in comment_display:
                fk = foreign_keys[key]
                fktable = fk.b.table
                counter[fktable.name] += 1
                alias = '%s_%d' % (fktable.name, counter[fktable.name])
                aliases[key] = alias
                fk_titles['%s_title' % key] = fktable.comment[COMMENT_TITLE].format(alias)
            
        def f(s): return s.format(self.alias, **fk_titles)

        comment_id = f(self.table.comment[COMMENT_ID])
        comment_title = f(self.table.comment[COMMENT_TITLE])
        comment_subtitle = f(self.table.comment[COMMENT_SUBTITLE])
        comment_order = map(f, self.table.comment[COMMENT_ORDER_BY])
        comment_search = map(f, self.table.comment[COMMENT_SEARCH])
        
        columns.append('%s %s' % (comment_id, 'id'))
        if comment_title != '*':
            columns.append('%s %s' % (comment_title, 'title'))
        columns.append('%s %s' % (comment_subtitle, 'subtitle'))
        for column in comment_display:
            columns.append('%s.%s' % (self.alias, column))

        if not comment_search:
            comment_search.append(comment_title)
            comment_search.append(comment_subtitle)
        logging.debug('Search columns: %s' % comment_search)
        
        logging.debug('Foreign keys: %s' % ', '.join(foreign_keys))
        for key in foreign_keys.keys():
            if key in comment_display:
                fk = foreign_keys[key]
                fktable = fk.b.table
                alias = aliases[key]
                title = fktable.comment[COMMENT_TITLE].format(alias)
                if title != '*':
                    columns.append(PROJECTION_FORMAT.format(title, fk.a.name))
                joins += JOIN_FORMAT.format(fk.b.table.name, alias, fk.b.name, self.alias, fk.a.name)

        if self.id:
            where = "%s = '%s'" % (comment_id, self.id)
        elif self.filter and comment_search:
            conjunctions = []
            for search_field in comment_search:
                conjunctions.append("%s ilike '%%%s%%'" % (search_field, self.filter))
            conjunctions.append("%s || '' = '%s'" % (comment_id, self.filter))
            where = OR_SEPARATOR.join(conjunctions)
        
        if not order:
            order.append(comment_id)

        return QUERY_FORMAT.format(self.table.name,
            LIST_SEPARATOR.join(columns),
            self.alias,
            joins,
            where,
            LIST_SEPARATOR.join(order),
            self.limit)
    
