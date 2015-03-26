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

from collections import OrderedDict

from dbnav.writer import FormatWriter
from dbnav.formatter import Formatter, DefaultFormatter


class VerboseGraphFormatter(DefaultFormatter):
    def __init__(self, options=None):
        DefaultFormatter.__init__(self)
        self.options = options

    def format_column_node(self, node):
        return node.format_verbose(self.options.verbose)


class GraphvizFormatter(DefaultFormatter):
    def format_name_node(self, item):
        return u'  root={0};'.format(item)

    def format_table_node(self, item):
        columns = map(
            lambda (i, it): u'<{1}> {1}'.format(i, it.name),
            enumerate(item.table.columns))
        return u'  {0} [shape="record" label="{0}| {1}"];'.format(
            item.table.name, '| '.join(columns))

    def format_foreign_key_node(self, item):
        return u'  {fk.a.tablename}:{fk.a.name} '\
            u'-> {fk.b.tablename}:{fk.b.name} [];'.format(fk=item.fk)


class GraphWriter(FormatWriter):
    def __init__(self, options=None):
        FormatWriter.__init__(self, u'{0}\n')
        if options.verbose > 0:
            Formatter.set(VerboseGraphFormatter(options))
        else:
            Formatter.set(DefaultFormatter())


class GraphvizWriter(FormatWriter):
    def __init__(self, include_tables=False):
        FormatWriter.__init__(self, u"""digraph dbgraph {{
{0}
}}
""")
        self.include_tables = include_tables
        Formatter.set(GraphvizFormatter())

    def filter_(self, items):
        # Removes duplicate items and keeps order
        return list(OrderedDict.fromkeys(items))


class GraphTestWriter(GraphWriter):
    pass
