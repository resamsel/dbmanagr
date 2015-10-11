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

from dbmanagr.logger import LogWith
from dbmanagr.utils import create_title

logger = logging.getLogger(__name__)


class Comment(object):
    def __init__(
            self, id_, title, subtitle, order, search, display, columns,
            aliases):
        self.id = id_
        self.title = title
        self.subtitle = subtitle
        self.order = order
        self.search = search
        self.display = display
        self.columns = columns
        self.aliases = aliases

    def __repr__(self):
        return unicode(self.__dict__)


@LogWith(logger)
def update_aliases(tablename, counter, aliases, foreign_keys):
    for key in filter(
            lambda k: foreign_keys[k].a.table.name == tablename,
            foreign_keys.keys()):
        fk = foreign_keys[key]
        fktable = fk.b.table
        if fktable.name in aliases:
            # We already know this alias
            continue
        aliases[fktable.name] = create_alias(fktable.name, counter)
    return aliases


@LogWith(logger)
def create_alias(tablename, counter):
    if tablename in counter:
        alias_format = u'_{0}{1}'
    else:
        alias_format = u'_{0}'
    counter[tablename] += 1
    return alias_format.format(tablename, counter[tablename])


@LogWith(logger)
def column_aliases(columns, alias):
    return dict(map(
        lambda col: (col.name, u'{{{0}_{1}}}'.format(alias, col.name)),
        columns))


def find_primary_key(table):
    if table.primary_key is None:
        # finds the primary key
        for c in table.columns():
            if c.primary_key:
                table.primary_key = c.name
                break

    return table.primary_key


def find_id(comment, caliases, alias, primary_key):
    if comment.id:
        return comment.id.format(**caliases)
    else:
        if primary_key:
            return u'{{{0}_{1}}}'.format(alias, primary_key)
        else:
            return "-"


@LogWith(logger)
def create_comment(table, comment, counter, aliases, alias):
    columns = {}
    display = []
    search = set(comment.search)

    logger.debug('search = set(%s)', comment.search)
    display.extend(comment.display)

    if table.name not in aliases:
        if alias:
            aliases[table.name] = alias
        else:
            aliases[table.name] = u'_{}'.format(table.name)

    alias = aliases[table.name]

    aliases = update_aliases(
        table.name,
        counter,
        aliases,
        table.foreign_keys())

    logger.debug('Aliases: %s', aliases)

    caliases = column_aliases(table.columns(), alias)
    for (_, v) in filter(
            lambda (k, v): v.a.table.name == table.name,
            table.foreign_keys().iteritems()):
        caliases.update(filter(
            lambda (k, v): k not in caliases.keys(),
            column_aliases(
                v.b.table.columns(), aliases[v.b.table.name]).iteritems()))

    logger.debug('Column aliases: %s', caliases)

    primary_key = find_primary_key(table)
    id_ = find_id(comment, caliases, alias, primary_key)

    title, subtitle, name = None, None, None
    if comment.title:
        title = comment.title.format(**caliases)
    else:
        name, title = create_title(comment, table.columns())
        d = dict(map(lambda k: (k.name, k.name), table.columns()))
        logger.debug('search.add(title.format(**d)=%s)', title.format(**d))
        search.add(title.format(**d))

        title = title.format(**caliases)

    if not subtitle:
        if comment.subtitle:
            subtitle = comment.subtitle.format(**caliases)
        else:
            _, subtitle = create_title(comment, table.columns(), [name])
            d = dict(map(lambda k: (k.name, k.name), table.columns()))
            logger.debug(
                'search.add(subtitle.format(**d)=%s)', subtitle.format(**d))
            search.add(subtitle.format(**d))

            subtitle = u'{0} (id={1})'.format(subtitle.format(**caliases), id_)

    if comment.order:
        order = comment.order
    else:
        order = []

    if display:
        display = map(lambda d: u'{0}_{1}'.format(alias, d), display)
    else:
        for column in table.columns():
            display.append(u'{0}_{1}'.format(alias, column.name))

    if primary_key in [c.name for c in table.columns()]:
        columns[primary_key] = id_
    else:
        columns[primary_key] = "'-'"

    if title != '*':
        columns['title'] = title

    columns['subtitle'] = subtitle
    for column in display:
        columns[column] = column

    return Comment(
        id_, title, subtitle, order, search, display, columns, aliases)
