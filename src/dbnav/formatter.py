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


class DefaultFormatter(object):
    def __init__(self):
        pass

    def format(self, item):
        return unicode(item)

    def format_item(self, item):
        return self.format(item)

    def format_row(self, item):
        return u', '.join(map(unicode, item))

    def format_column(self, item):
        return self.format(item)

    def format_node(self, item):
        return unicode(item)

    def format_column_node(self, item):
        return self.format(item)

    def format_name_node(self, item):
        return self.format(item)

    def format_table_node(self, item):
        return self.format(item)

    def format_foreign_key_node(self, item):
        return self.format(item)


class SimplifiedFormatter(DefaultFormatter):
    def __init__(
            self,
            default_format=u'{title}\t{subtitle}',
            item_format=u'{title}\t{subtitle}'):
        self.default_format = default_format
        self.item_format = item_format

    def format(self, item):
        return self.default_format.format(
            title=self.escape(item.title()),
            subtitle=self.escape(item.subtitle()),
            autocomplete=self.escape(item.autocomplete()),
            uid=self.escape(item.uid()),
            validity=self.escape(item.validity()),
            icon=self.escape(item.icon()),
            value=self.escape(item.value()))

    def format_row(self, item):
        return self.format(item)

    def escape(self, value):
        return value


class TestFormatter(SimplifiedFormatter):
    def format(self, item):
        return u'{title}\t{autocomplete}'.format(
            title=item.title(),
            autocomplete=item.autocomplete())


class JsonFormatter(SimplifiedFormatter):
    def __init__(self):
        SimplifiedFormatter.__init__(
            self,
            default_format=u'   {{ '
                           u'"uid": "{uid}", '
                           u'"arg": "{title}", '
                           u'"autocomplete": "{autocomplete}", '
                           u'"valid": "{validity}", '
                           u'"title": "{title}", '
                           u'"subtitle": "{subtitle}", '
                           u'"icon": "{icon}" '
                           u'}}',
            item_format=u'   {{ '
                        u'"uid": "{uid}", '
                        u'"arg": "{title}", '
                        u'"autocomplete": '
                        u'"{autocomplete}", '
                        u'"valid": "{validity}", '
                        u'"title": "{title}", '
                        u'"subtitle": "{subtitle}", '
                        u'"icon": "{icon}" '
                        u'}}')


class SimpleFormatter(SimplifiedFormatter):
    def __init__(self):
        SimplifiedFormatter.__init__(
            self,
            default_format=u"""{uid}\t{title}\t{subtitle}\t{autocomplete}""",
            item_format=u"""{uid}\t{title}\t{subtitle}\t{autocomplete}""")


class AutocompleteFormatter(SimplifiedFormatter):
    def __init__(self):
        SimplifiedFormatter.__init__(
            self,
            default_format=u"""{autocomplete}""",
            item_format=u"""{autocomplete}""")


class Formatter(object):
    formatter = DefaultFormatter()

    @staticmethod
    def set(arg):
        Formatter.formatter = arg

    @staticmethod
    def format(item):
        return Formatter.formatter.format(item)

    @staticmethod
    def format_row(item):
        return Formatter.formatter.format_row(item)

    @staticmethod
    def format_column(item):
        return Formatter.formatter.format_column(item)

    @staticmethod
    def format_node(item):
        return Formatter.formatter.format_node(item)

    @staticmethod
    def format_column_node(item):
        return Formatter.formatter.format_column_node(item)

    @staticmethod
    def format_table_node(item):
        return Formatter.formatter.format_table_node(item)

    @staticmethod
    def format_name_node(item):
        return Formatter.formatter.format_name_node(item)

    @staticmethod
    def format_foreign_key_node(item):
        return Formatter.formatter.format_foreign_key_node(item)
