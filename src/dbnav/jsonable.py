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

from dbnav.exception import BusinessException


def as_json(obj):
    if isinstance(obj, datetime.datetime) or isinstance(obj, datetime.date):
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
    if isinstance(obj, dict):
        return dict(map(lambda (k, v): (k, as_json(v)), obj.iteritems()))
    if isinstance(obj, tuple):
        return map(as_json, obj)
    if isinstance(obj, Jsonable):
        d = {
            '__cls__': str(obj.__class__)
        }
        for key, value in obj.__dict__.iteritems():
            if not key.startswith('_'):
                if isinstance(value, Jsonable):
                    d[key] = value.as_json()
                else:
                    d[key] = as_json(value)
        return d
    return obj


def import_class(name):
    parts = name.split('.')
    mod = __import__('.'.join(parts[:-1]), fromlist=[str(parts[-1])])
    return getattr(mod, parts[-1])


def from_json(d):
    if type(d) is dict:
        if '__cls__' in d:
            classname = d['__cls__']
            if classname.endswith('Exception'):
                return BusinessException(d['message'])
            if classname == 'sqlalchemy.util.KeyedTuple':
                from sqlalchemy.util import KeyedTuple
                return KeyedTuple(
                    map(lambda k: from_json(d[k]), d['_labels']),
                    labels=d['_labels'])
            if classname == 'datetime.datetime':
                from datetime import datetime
                return datetime.strptime(d['value'], "%Y-%m-%dT%H:%M:%S")
            if classname == 'datetime.date':
                from datetime import datetime
                return datetime.strptime(d['value'], "%Y-%m-%d").date()
            cls = import_class(classname)
            if hasattr(cls, 'from_json'):
                return cls.from_json(d)
        return dict(map(lambda (k, v): (k, from_json(v)), d.iteritems()))
    if type(d) is list or type(d) is tuple:
        return map(from_json, d)
    return d


class Jsonable:
    def as_json(self):
        return as_json(self)
