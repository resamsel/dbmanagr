#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from dbnav.writer import FormatWriter
from dbnav.formatter import Formatter, DefaultFormatter, GraphvizFormatter


class VerboseGraphFormatter(DefaultFormatter):
    def __init__(self, options=None):
        DefaultFormatter.__init__(self)
        self.options = options

    def format_column_node(self, node):
        return node.format_verbose(self.options.verbose)


class GraphWriter(FormatWriter):
    def __init__(self, options=None):
        FormatWriter.__init__(self, u'{0}')
        if options.verbose > 0:
            Formatter.set(VerboseGraphFormatter(options))
        else:
            Formatter.set(DefaultFormatter())


class GraphvizWriter(FormatWriter):
    def __init__(self, include_tables=False):
        FormatWriter.__init__(self, u"""digraph dbgraph {{
{0}
}}""")
        self.include_tables = include_tables
        Formatter.set(GraphvizFormatter())

    def filter(self, items):
        # Removes duplicate items and keeps order
        return list(OrderedDict.fromkeys(items))


class GraphTestWriter(GraphWriter):
    pass
