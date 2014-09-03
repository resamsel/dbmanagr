#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict

from dbnav.writer import FormatWriter
from dbnav.formatter import Formatter, GraphvizFormatter
from dbnav.node import ColumnNode

class GraphvizWriter(FormatWriter):
    def __init__(self):
        FormatWriter.__init__(self, u"""digraph dbgraph {{
{0}
}}""")
        Formatter.set(GraphvizFormatter())
    def filter(self, items):
        # Removes duplicate items and keeps order
        return list(OrderedDict.fromkeys(
            filter(lambda i: not isinstance(i, ColumnNode), items)))
