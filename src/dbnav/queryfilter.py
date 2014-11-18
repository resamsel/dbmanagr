#!/usr/bin/env python
# -*- coding: utf-8 -*-


class QueryFilter:
    def __init__(self, lhs, operator=None, rhs=None):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def __str__(self):
        return 'lhs={self.lhs}, op={self.operator}, rhs={self.rhs}'.format(
            self=self)
