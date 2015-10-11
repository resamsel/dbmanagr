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
import codecs
import sys

from dbmanagr.logger import LogWith
from dbmanagr.formatter import Formatter, TestFormatter, DefaultFormatter

UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

logger = logging.getLogger(__name__)


class DefaultWriter(object):
    def write(self, items):
        return self.str(items)

    def str(self, items):
        return map(self.itemtostring, items)

    def itemtostring(self, item):
        return unicode(item)


class StdoutWriter(DefaultWriter):
    def __init__(
            self,
            items_format=u"Title\tSubtitle\tAutocomplete\n{0}\n",
            item_format=u"{title}\t{subtitle}\t{autocomplete}",
            item_separator=u"\n",
            format_error_format=u'{0}'):
        self.items_format = items_format
        self.item_format = item_format
        self.item_separator = item_separator
        self.format_error_format = format_error_format

        Formatter.set(DefaultFormatter())

    def filter_(self, items):
        return items

    def str(self, items):
        items = self.prepare(items)
        items = self.filter_(items)
        s = self.item_separator.join(map(self.itemtostring, items))
        return self.items_format.format(s)

    def prepare(self, items):
        if not items:
            return []
        return items

    def itemtostring(self, item):
        return self.item_format.format(
            item=unicode(item), **item.__dict__)


class FormatWriter(StdoutWriter):
    def __init__(
            self,
            items_format=u"""Title\tSubtitle\tAutocomplete
{0}
""",
            item_format=u"""{title}\t{subtitle}\t{autocomplete}""",
            item_separator=u"""
""",
            format_error_format=u'{0}'):
        StdoutWriter.__init__(
            self,
            items_format,
            item_format,
            item_separator,
            format_error_format)

    def itemtostring(self, item):
        return item.format()


class TestWriter(FormatWriter):
    def __init__(
            self,
            items_format=u"""Title\tAutocomplete
{0}""",
            item_format=u"""{title}\t{autocomplete}"""):
        FormatWriter.__init__(self, items_format, item_format)
        Formatter.set(TestFormatter())


class Writer(object):
    writer = StdoutWriter()

    @staticmethod
    def set(arg):
        Writer.writer = arg

    @staticmethod
    @LogWith(logger, log_args=False, log_result=False)
    def write(items):
        return Writer.writer.write(items)

    @staticmethod
    @LogWith(logger, log_args=False, log_result=False)
    def itemtostring(item):
        return Writer.writer.itemtostring(item)
