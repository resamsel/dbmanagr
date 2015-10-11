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

__drivers__ = []

KIND_VALUE = 'value'
KIND_FOREIGN_KEY = 'foreign-key'
KIND_FOREIGN_VALUE = 'foreign-value'

IMAGE_VALUE = 'images/value.png'
IMAGE_FOREIGN_KEY = 'images/foreign-key.png'
IMAGE_FOREIGN_VALUE = 'images/foreign-value.png'

OPTION_URI_SINGLE_ROW_FORMAT = u'%s%s/?%s'
OPTION_URI_MULTIPLE_ROWS_FORMAT = u'%s%s?%s'

OPERATORS = {
    '=': lambda c, v: c.__eq__(v),
    '!=': lambda c, v: c.__ne__(v),
    '~': lambda c, v: c.like(v),
    '*': lambda c, v: c.like(v),
    '>': lambda c, v: c.__gt__(v),
    '>=': lambda c, v: c.__ge__(v),
    '<=': lambda c, v: c.__le__(v),
    '<': lambda c, v: c.__lt__(v),
    'in': lambda c, v: c.in_(v),
    ':': lambda c, v: c.in_(v)
}
