#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from dbnav.logger import LogWith
from dbnav.utils import create_title

logger = logging.getLogger(__name__)


@LogWith(logger)
def populate_titles(
        connection, display, counter, aliases, fk_titles, foreign_keys):
    for key in filter(
            lambda k: k in display,
            foreign_keys.keys()):
        fk = foreign_keys[key]
        fktable = fk.b.table
        counter[fktable.name] += 1
        alias = '%s_%d' % (fktable.name, counter[fktable.name])
        aliases[key] = alias
        k = '%s_title' % key
        try:
            comment = connection.comment(fktable.name)
            if comment.title:
                fk_titles[k] = comment.title.format(alias)
        except KeyError:
            fk_titles[k] = "'columns[k_]'"


def create_comment(table, comment, counter, aliases, alias):
    fk_titles = {}
    columns = {}
    display = comment.display
    table.primary_key = None

    # finds the primary key
    for c in table.columns():
        if c.primary_key:
            table.primary_key = c.name
            break

    if not comment.id and table.primary_key:
        comment.id = '{%s}' % table.primary_key
    if not comment.id:
        comment.id = "-"

    if not display:
        for column in table.columns():
            display.append(column.name)

    populate_titles(
        table.connection,
        display,
        counter,
        aliases,
        fk_titles,
        table.fks)

    if not comment.title:
        name, title = create_title(comment, table.columns(), fk_titles)
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

    id = comment.id
    title = comment.title
    subtitle = comment.subtitle
    order = comment.order
    search = comment.search

    if table.primary_key in [c.name for c in table.columns()]:
        columns[table.primary_key] = id
    else:
        columns[table.primary_key] = "'-'"
    if title != '*':
        columns['title'] = title
    columns['subtitle'] = subtitle
    for column in display:
        columns[column] = column

    if not search:
        d = dict(map(lambda k: (str(k), k), columns.keys()))
        search.append(title.format(table.name, **d))

    return Comment(id, title, subtitle, order, search, display, columns)


class Comment:
    def __init__(self, id, title, subtitle, order, search, display, columns):
        self.id = id
        self.title = title
        self.subtitle = subtitle
        self.order = order
        self.search = search
        self.display = display
        self.columns = columns

    def __repr__(self):
        return unicode(self.__dict__)
