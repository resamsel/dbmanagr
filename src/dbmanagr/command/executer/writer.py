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

from dbmanagr.writer import FormatWriter, StdoutWriter
from dbmanagr.formatter import Formatter, DefaultFormatter
import datetime

import pprint
pp = pprint.PrettyPrinter(indent=4)


def sql_escape(value):
    if type(value) is str or type(value) is unicode:
        return "'%s'" % value
    if type(value) in [datetime.datetime, datetime.date, datetime.time]:
        return "'%s'" % value
    if type(value) is bool:
        return unicode(value).lower()
    return unicode(value)


class ExecuteWriter(StdoutWriter):
    def __init__(self, options=None):
        StdoutWriter.__init__(self, u'{0}\n', u'{item}')
        Formatter.set(DefaultFormatter())
        self.options = options


class SqlInsertWriter(FormatWriter):
    def __init__(self, options=None):
        FormatWriter.__init__(
            self,
            u'{0}\n',
            u'insert into {table} ({columns}) values ({values});')
        Formatter.set(DefaultFormatter())
        self.table_name = options.table_name

    def itemtostring(self, item):
        row = item.row
        return self.item_format.format(
            table=self.table_name,
            columns=self.create_columns(row.keys()),
            values=self.create_values(row.values()))

    def create_columns(self, cols):
        return u','.join(map(unicode, cols))

    def create_values(self, values):
        return u','.join(map(sql_escape, values))


class ExecuteTestWriter(ExecuteWriter):
    pass
