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

from dbmanagr.writer import FormatWriter, TabularWriter
from dbmanagr.formatter import Formatter, AutocompleteFormatter
from dbmanagr.formatter import JsonFormatter, SimpleFormatter, \
    SimplifiedFormatter


class SimplifiedWriter(TabularWriter):
    def __init__(self):
        super(SimplifiedWriter, self).__init__(
            None,
            lambda items: [],
            lambda item: [item.title(), item.subtitle()]
        )


class JsonWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(
            self,
            u"""[
{0}
]
""", item_separator=u',\n',)
        Formatter.set(JsonFormatter())


class AutocompleteWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u'{0}', u'{autocomplete}')
        Formatter.set(AutocompleteFormatter())


class SimpleWriter(TabularWriter):
    def __init__(self):
        super(SimpleWriter, self).__init__(
            None,
            lambda items: [u'Id', u'Title', u'Subtitle', u'Autocomplete'],
            lambda item: [
                item.uid(), item.title(), item.subtitle(), item.autocomplete()
            ]
        )
