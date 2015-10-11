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

from dbmanagr.writer import FormatWriter
from dbmanagr.formatter import Formatter, DefaultFormatter


def value_from_column(column, config):
    if config.verbose > 3:
        return '{0}?{1}'.format(
            column.autocomplete().split('?')[0], column.ddl())
    if config.verbose > 2:
        return column.autocomplete()
    if config.verbose > 1:
        return '/'.join(column.autocomplete().split('/')[1:])
    if config.verbose > 0:
        return unicode(column)
    return column_name(column, config)


def column_name(column, config):
    if config.compare_ddl:
        return column.ddl()
    return column.name


class DiffWriter(FormatWriter):
    def __init__(self, left=None, right=None):
        FormatWriter.__init__(self, u'{0}\n')
        Formatter.set(DefaultFormatter())
        self.left = left
        self.right = right

    def str(self, items):
        items = [i for i in items]  # resolves generator
        if not items:
            return self.items_format.format('No differences found')
        s = self.item_separator.join(
            map(self.itemtostring, self.filter_(items)))
        return self.items_format.format(s)

    def itemtostring(self, item):
        """We receive a tuple (left, right), for which any part may be empty"""
        left, right = item
        a = []
        if left:
            a.append(u'< {0}'.format(value_from_column(left, self.left)))
        if right:
            a.append(u'> {0}'.format(value_from_column(right, self.right)))
        return u'\n'.join(a)


class DiffColumnWriter(DiffWriter):
    def __init__(self, left=None, right=None):
        DiffWriter.__init__(self, left, right)
        self.left = left
        self.right = right

    def itemtostring(self, item):
        """We receive a tuple (left, right), for which any part may be empty"""
        left, right = item
        s = ''
        if left:
            val = value_from_column(left, self.left)
            s += u'{1}{0}'.format(u' ' * (42 - len(val)), val)
            if right:
                s += ' | '
        else:
            s += u'{0} > '.format(u' ' * 42)
        if right:
            val = value_from_column(right, self.right)
            s += val
        else:
            s += ' <'
        return s


class DiffTestWriter(DiffWriter):
    pass
