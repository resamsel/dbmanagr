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

import datetime
import sqlalchemy
import re

from decimal import Decimal

from dbmanagr.exception import BusinessException


def to_key(key):
    return re.sub(r"_+$", '', key)


def as_json(obj):
    if isinstance(obj, (int, long, float, bool)) or obj is None:
        return obj
    if isinstance(obj, dict):
        return dict(map(
            lambda (k, v): (to_key(k), as_json(v)),
            obj.iteritems())
        )
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return {
            '__cls__': 'datetime.{}'.format(obj.__class__.__name__),
            'value': obj.isoformat()
        }
    if isinstance(obj, sqlalchemy.util.KeyedTuple):
        d = {
            '__cls__': 'sqlalchemy.util.KeyedTuple'
        }
        d.update(dict(map(as_json, obj.__dict__.iteritems())))
        return d
    if isinstance(obj, sqlalchemy.sql.sqltypes.NullType):
        return None
    if isinstance(obj, (tuple, list, set)):
        return map(as_json, obj)
    if isinstance(obj, Jsonable):
        d = {
            '__cls__': str(obj.__class__)
        }
        for key, value in obj.__dict__.iteritems():
            if not key.startswith('_'):
                if isinstance(value, Jsonable):
                    d[to_key(key)] = value.as_json()
                else:
                    d[to_key(key)] = as_json(value)
        return d
    return unicode(obj)


def import_class(name):
    parts = name.split('.')
    if len(parts) > 1:
        mod = __import__('.'.join(parts[:-1]), fromlist=[str(parts[-1])])
        return getattr(mod, parts[-1])
    return None


def from_json(d):
    if type(d) is dict:
        if '__cls__' in d:
            classname = d['__cls__']
            if (classname.endswith('Exception')
                    or classname.endswith('Error')
                    or classname.endswith('Exit')):
                return BusinessException(d['message'])
            if classname == 'sqlalchemy.util.KeyedTuple':
                from sqlalchemy.util import KeyedTuple
                return KeyedTuple(
                    map(lambda k: from_json(d[k]), d['_labels']),
                    labels=d['_labels'])
            if classname == 'datetime.datetime':
                from datetime import datetime
                try:
                    return datetime.strptime(d['value'], "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    return datetime.strptime(
                        d['value'], "%Y-%m-%dT%H:%M:%S.%f")
            if classname == 'datetime.date':
                from datetime import datetime
                return datetime.strptime(d['value'], "%Y-%m-%d").date()
            cls = import_class(classname)
            if hasattr(cls, 'from_json'):
                return cls.from_json(d)
        return dict(map(lambda (k, v): (k, from_json(v)), d.iteritems()))
    if type(d) is list or type(d) is tuple:
        return map(from_json, d)
    if type(d) is Decimal:
        if d % 1 == 0:
            return int(d)
        else:
            return float(d)
    return d


class Jsonable(object):
    def as_json(self):
        return as_json(self)
