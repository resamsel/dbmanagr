#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xml.sax import saxutils


class DefaultFormatter:
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
        return self.format(item)

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

    def format_item(self, item):
        return self.item_format.format(
            title=self.escape(item.title),
            subtitle=self.escape(item.subtitle),
            autocomplete=self.escape(item.autocomplete),
            uid=self.escape(item.uid),
            validity=self.escape(
                {True: 'yes', False: 'no'}.get(item.validity, 'yes')),
            icon=self.escape(item.icon),
            value=self.escape(item.value))

    def format_row(self, item):
        return self.format(item)

    def escape(self, value):
        return value


class TestFormatter(SimplifiedFormatter):
    def format(self, item):
        return u'{title}\t{autocomplete}'.format(
            title=item.title(),
            autocomplete=item.autocomplete())

    def format_item(self, item):
        return u'{title}\t{autocomplete}'.format(
            title=item.title,
            autocomplete=item.autocomplete)


class GraphvizFormatter(DefaultFormatter):
    def format_name_node(self, item):
        return u'  root={0};'.format(item)

    def format_table_node(self, item):
        columns = map(
            lambda (i, it): u'<{1}> {1}'.format(i, it.name),
            enumerate(item.table.columns()))
        return u'  {0} [shape="record" label="{0}| {1}"];'.format(
            item.table.name, '| '.join(columns))

    def format_foreign_key_node(self, item):
        return u'  {fk.a.table.name}:{fk.a.name} '\
            u'-> {fk.b.table.name}:{fk.b.name} [];'.format(fk=item)


class XmlFormatter(SimplifiedFormatter):
    def __init__(self):
        SimplifiedFormatter.__init__(
            self,
            default_format=u"""   <item
            uid="{uid}"
            arg="{value}"
            autocomplete="{autocomplete}"
            valid="{validity}">
        <title>{title}</title>
        <subtitle>{subtitle}</subtitle>
        <icon>{icon}</icon>
    </item>""",
            item_format=u"""   <item
            uid="{uid}"
            arg="{value}"
            autocomplete="{autocomplete}"
            valid="{validity}">
        <title>{title}</title>
        <subtitle>{subtitle}</subtitle>
        <icon>{icon}</icon>
    </item>""")

    def escape(self, value):
        if type(value) == str or type(value) == unicode:
            return saxutils.escape(value)
        return saxutils.escape(unicode(value))


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


class Formatter:
    formatter = DefaultFormatter()

    @staticmethod
    def set(arg):
        Formatter.formatter = arg

    @staticmethod
    def format(item):
        return Formatter.formatter.format(item)

    @staticmethod
    def format_item(item):
        return Formatter.formatter.format_item(item)

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
