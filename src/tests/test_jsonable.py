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

from tests.testcase import ParentTestCase
from dbmanagr import jsonable


class TestJsonable(jsonable.Jsonable):
    def __init__(self):
        self.a = 1
        self.b = jsonable.Jsonable()


class JsonableTestCase(ParentTestCase):
    def test_to_key(self):
        """Tests the jsonable.to_key function"""

        self.assertEqual('a', jsonable.to_key('a_'))

    def test_as_json(self):
        """Tests the jsonable.as_json function"""

        self.assertEqual(None, jsonable.as_json(None))
        self.assertEqual({}, jsonable.as_json({}))

        import datetime
        obj = datetime.datetime(2014, 5, 5)
        self.assertEqual(
            {
                '__cls__': 'datetime.datetime',
                'value': obj.isoformat()
            },
            jsonable.as_json(obj)
        )

        from sqlalchemy.util import KeyedTuple
        self.assertEqual(
            {
                '__cls__': 'sqlalchemy.util.KeyedTuple',
                '_labels': ['a'],
                'a': 1
            },
            jsonable.as_json(KeyedTuple([1], labels=['a']))
        )

        from sqlalchemy.sql.sqltypes import NullType
        self.assertEqual(None, jsonable.as_json(NullType()))

        self.assertEqual([1], jsonable.as_json([1]))
        self.assertEqual(u'a', jsonable.as_json('a'))

        self.assertEqual(
            {
                '__cls__': "<class 'tests.test_jsonable.TestJsonable'>",
                'a': 1,
                'b': {
                    '__cls__': "<class 'dbmanagr.jsonable.Jsonable'>"
                }
            },
            jsonable.as_json(TestJsonable())
        )

    def test_import_class(self):
        """Tests the jsonable.import_class function"""

        self.assertEqual(None, jsonable.import_class('a'))
        self.assertIsNotNone(jsonable.import_class('dbmanagr.utils'))

    def test_from_json(self):
        """Tests the jsonable.from_json function"""

        self.assertEqual(None, jsonable.from_json(None))
        self.assertEqual({}, jsonable.from_json({}))
        self.assertEqual([], jsonable.from_json([]))

        self.assertEqual({'a': 1}, jsonable.from_json({'a': 1}))
        self.assertEqual([1], jsonable.from_json([1]))
        self.assertEqual([1], jsonable.from_json((1,)))

        from decimal import Decimal
        self.assertEqual(1, jsonable.from_json(Decimal(1)))
        self.assertEqual(1.1, jsonable.from_json(Decimal(1.1)))

        import datetime
        obj = datetime.datetime(2014, 5, 5)
        self.assertEqual(
            obj,
            jsonable.from_json({
                '__cls__': 'datetime.datetime',
                'value': obj.isoformat()
            })
        )
        self.assertEqual(
            obj,
            jsonable.from_json({
                '__cls__': 'datetime.datetime',
                'value': '2014-05-05T00:00:00.000'
            })
        )
        self.assertEqual(
            obj.date(),
            jsonable.from_json({
                '__cls__': 'datetime.date',
                'value': '2014-05-05'
            })
        )

        self.assertEqual(
            'a',
            jsonable.from_json({
                '__cls__': 'a.Exception',
                'message': 'a'
            }).message
        )

        from sqlalchemy.util import KeyedTuple
        self.assertEqual(
            KeyedTuple([1], labels=['a']),
            jsonable.from_json({
                '__cls__': 'sqlalchemy.util.KeyedTuple',
                '_labels': ['a'],
                'a': 1
            })
        )

        from dbmanagr.dto.node import NameNode
        self.assertEqual(
            NameNode('a'),
            jsonable.from_json({
                '__cls__': 'dbmanagr.dto.node.NameNode',
                'name': 'a',
                'indent': 0
            })
        )
