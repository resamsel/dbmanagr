#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from dbnav.utils import create_title

logger = logging.getLogger(__name__)


class Comment:
    def __init__(self, table, comment, counter, aliases, alias):
        self.table = table
        self.counter = counter
        self.aliases = aliases
        self.alias = alias

        self.fk_titles = {}
        self.columns = {}
        self.display = comment.display

        self.build(comment)

    def build(self, comment):
        table = self.table

        table.primary_key = None

        columns = table.columns()

        # finds the primary key
        for c in columns:
            if c.primary_key:
                table.primary_key = c.name
                break

        if not comment.id and table.primary_key:
            comment.id = '{%s}' % table.primary_key
        if not comment.id:
            comment.id = "-"

        if not self.display:
            for column in columns:
                self.display.append(column.name)

        self.populate_titles(self.fk_titles, table.fks)

        if not comment.title:
            name, title = create_title(comment, columns, self.fk_titles)
            comment.title = title
            if name == table.primary_key:
                comment.subtitle = "'%s'" % name
            else:
                comment.subtitle = "{%s} (id=%s)" % (name, comment.id)
        if not comment.subtitle:
            if table.primary_key:
                comment.subtitle = "'%s'" % table.primary_key
            else:
                comment.subtitle = "'There is no primary key'"

        self.id = comment.id
        self.title = comment.title
        self.subtitle = comment.subtitle
        self.order = comment.order
        self.search = comment.search

        if table.primary_key in [c.name for c in columns]:
            self.columns[table.primary_key] = self.id
        else:
            self.columns[table.primary_key] = "'-'"
        if self.title != '*':
            self.columns['title'] = self.title
        self.columns['subtitle'] = self.subtitle
        for column in self.display:
            self.columns[column] = column

        if not self.search:
            d = dict(map(lambda k: (str(k), k), self.columns.keys()))
            self.search.append(self.title.format(self.table.name, **d))

    def populate_titles(self, fk_titles, foreign_keys):
        # logger.debug("Populate titles: %s", foreign_keys.keys())
        connection = self.table.connection
        for key in filter(
                lambda k: k in self.display,
                foreign_keys.keys()):
            fk = foreign_keys[key]
            fktable = fk.b.table
            self.counter[fktable.name] += 1
            alias = '%s_%d' % (fktable.name, self.counter[fktable.name])
            self.aliases[key] = alias
            k = '%s_title' % key
            try:
                comment = connection.comment(fktable.name)
                if comment.title:
                    fk_titles[k] = comment.title.format(alias)
            except KeyError:
                fk_titles[k] = "'columns[k_]'"

    def __repr__(self):
        return unicode(self.__dict__)
