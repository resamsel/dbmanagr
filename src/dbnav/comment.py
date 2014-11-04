#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy.types import Integer

from dbnav.logger import logger


class Comment:
    def __init__(self, table, counter, aliases, alias):
        self.table = table
        self.counter = counter
        self.aliases = aliases
        self.alias = alias

        comment = table.comment

        self.fk_titles = {}
        self.columns = {}
        self.display = comment.display
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
            name, title = self.create_title(comment, columns)
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

        def f(s):
            try:
                return s.format(self.alias, **self.fk_titles)
            except KeyError, e:
                logger.debug("Foreign key titles: %s" % self.fk_titles)
                logger.error("Error: %s" % e)
                return s

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
            self.search.append(self.title.format(**d))

    def __repr__(self):
        return str(self.__dict__)

    def create_title(self, comment, columns):
        logger.debug('create_title(comment=%s, columns=%s)', comment, columns)

        # find specially named columns (but is not an integer - integers are no good names)
        for c in columns:
            for name in ['name', 'title', 'key', 'text', 'username', 'user_name', 'email', 'comment']:
                if c.name == name:
                    if not isinstance(c.type, Integer):
                        return (name, '{%s}' % c.name)
                    elif '%s_title' % name in self.fk_titles:
                        return ('%s_title' % name, self.fk_titles['%s_title' % name])

        # find columns that end with special names
        for c in columns:
            for name in ['name', 'title', 'key', 'text']:
                if c.name.endswith(name) and not isinstance(c.type, Integer):
                    return (name, '{%s}' % c.name)

        if comment.id:
            return ('id', '{%s}' % comment.id)

        return ('First column', '{%s}' % columns[0].name)

    def populate_titles(self, fk_titles, foreign_keys):
        # logger.debug("Populate titles: %s", foreign_keys.keys())
        for key in foreign_keys.keys():
            if key in self.display:
                fk = foreign_keys[key]
                fktable = fk.b.table
                self.counter[fktable.name] += 1
                alias = '%s_%d' % (fktable.name, self.counter[fktable.name])
                self.aliases[key] = alias
                k = '%s_title' % key
                try:
                    if fktable.comment.title:
                        fk_titles[k] = fktable.comment.title.format(alias)
                except KeyError:
                    fk_titles[k] = "'columns[k_]'"
