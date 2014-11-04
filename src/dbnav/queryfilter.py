#!/usr/bin/env python
# -*- coding: utf-8 -*-


class QueryFilter:
    def __init__(self, lhs, operator=None, rhs=None):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs