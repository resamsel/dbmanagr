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

from dbnav.logger import LogWith
from dbnav.utils import create_title

logger = logging.getLogger(__name__)


class Comment:
    def __init__(
            self, id, title, subtitle, order, search, display, columns,
            aliases):
        self.id = id
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
        if fktable.name in counter:
            alias_format = u'_{0}{1}'
        else:
            alias_format = u'_{0}'
        counter[fktable.name] += 1
        aliases[fktable.name] = alias_format.format(
            fktable.name, counter[fktable.name])
    return aliases


@LogWith(logger)
def column_aliases(columns, alias):
    return dict(map(
        lambda col: (col.name, u'{{{0}_{1}}}'.format(alias, col.name)),
        columns))


@LogWith(logger)
def create_comment(table, comment, counter, aliases, alias):
    columns = {}
    display = []
    search = []

    display.extend(comment.display)
    search.extend(comment.search)

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
    for (k, v) in filter(
            lambda (k, v): v.a.table.name == table.name,
            table.foreign_keys().iteritems()):
        caliases.update(filter(
            lambda (k, v): k not in caliases.keys(),
            column_aliases(
                v.b.table.columns(), aliases[v.b.table.name]).iteritems()))

    logger.debug('Column aliases: %s', caliases)

    if table.primary_key is None:
        # finds the primary key
        for c in table.columns():
            if c.primary_key:
                table.primary_key = c.name
                break

    primary_key = table.primary_key

    if comment.id:
        id = comment.id.format(**caliases)
    else:
        if primary_key:
            id = u'{{{0}_{1}}}'.format(alias, primary_key)
        else:
            id = "-"

    title, subtitle, name = None, None, None
    if comment.title:
        title = comment.title.format(**caliases)
    else:
        name, title = create_title(comment, table.columns())
        d = dict(map(lambda k: (k.name, k.name), table.columns()))
        search.append(title.format(**d))

        title = title.format(**caliases)

    if not subtitle:
        if comment.subtitle:
            subtitle = comment.subtitle.format(**caliases)
        else:
            sname, subtitle = create_title(comment, table.columns(), [name])
            d = dict(map(lambda k: (k.name, k.name), table.columns()))
            search.append(subtitle.format(**d))

            subtitle = u'{0} (id={1})'.format(subtitle.format(**caliases), id)

        if not subtitle:
            if name == primary_key:
                subtitle = u"'%s'" % name
            else:
                subtitle = u"%s (id=%s)" % (caliases[name], id)

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
        columns[primary_key] = id
    else:
        columns[primary_key] = "'-'"

    if title != '*':
        columns['title'] = title

    columns['subtitle'] = subtitle
    for column in display:
        columns[column] = column

    return Comment(
        id, title, subtitle, order, search, display, columns, aliases)
