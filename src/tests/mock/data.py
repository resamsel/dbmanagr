#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbnav.model.column import Column
from dbnav.model.foreignkey import ForeignKey
from dbnav.model.table import Table


class MockEntity:
    def __init__(self, name):
        self.name = name

FOREIGN_KEYS = {
    't1.c1 -> t2.c2': ForeignKey(
        Column(Table(
            None, None, MockEntity('t1')), 'c1', type=str),
        Column(Table(
            None, None, MockEntity('t2')), 'c2', type=str)),
    't1.c3 -> t3.c1': ForeignKey(
        Column(Table(
            None, None, MockEntity('t1')), 'c3', type=str),
        Column(Table(
            None, None, MockEntity('t3')), 'c1', type=str)),
    't2.c3 -> t4.c1': ForeignKey(
        Column(Table(
            None, None, MockEntity('t2')), 'c3', type=str),
        Column(Table(
            None, None, MockEntity('t4')), 'c1', type=str))
}
