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


class Op(object):
    def last(self):
        return None

    def __str__(self):
        return self.__repr__()


class QueryFilter(Op):
    def __init__(self, lhs, operator=None, rhs=None):
        self.lhs = lhs
        self.operator = operator
        self.rhs = rhs

    def last(self):
        return self

    def __repr__(self):
        return '{me.lhs} {me.operator} {me.rhs}'.format(
            me=self)


class BitOp(Op):
    def __init__(self, children=None):
        if children is not None:
            self.children = children
        else:
            self.children = []

    def append(self, _filter):
        self.children.append(_filter)

    def last(self):
        return self.children[-1].last()

    def __getitem__(self, i):
        return self.children[i]

    def __len__(self):
        return len(self.children)


class OrOp(BitOp):
    def __repr__(self):
        return u' or '.join(map(unicode, self.children))


class AndOp(BitOp):
    def __repr__(self):
        return u' and '.join(map(unicode, self.children))
