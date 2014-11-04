#!/usr/bin/env python
# -*- coding: utf-8 -*-


class ForeignKey:
    """A foreign key connection between the originating column a and the foreign column b"""

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return '%s -> %s' % (self.a, self.b)

