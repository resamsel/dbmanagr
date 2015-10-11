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

from tests.testcase import DbTestCase
from dbmanagr.driver.postgresql import driver


class OptionsTestCase(DbTestCase):
    def test_restriction(self):
        """Tests the postgresql restriction function"""

        con = DbTestCase.connection
        article = con.table('article')

        self.assertEqual(
            '_article.id = 1',
            driver.restriction(
                '_article', article.column('id'), '~', 1))
        self.assertEqual(
            "cast(_article.id as text) ~ 's'",
            driver.restriction(
                '_article', article.column('id'), '~', 's'))
        self.assertEqual(
            '_article.id is null',
            driver.restriction(
                '_article', article.column('id'), '=', None))
        self.assertEqual(
            'id is null',
            driver.restriction(
                None, article.column('id'), '=', None))
        self.assertRaises(
            Exception,
            driver.restriction,
            None,
            None,
            None,
            None
        )

    def test_driver_restriction(self):
        """Tests the postgresql driver restriction function"""

        con = DbTestCase.connection
        article = con.table('article')

        self.assertEqual(
            '_article.id = 1',
            driver.PostgreSQLDriver().restriction(
                '_article', article.column('id'), '~', 1))

    def test_statement_activity(self):
        """Tests the postgresql driver statement_activity function"""

        con = DbTestCase.connection

        self.assertRaises(
            Exception,
            driver.PostgreSQLDriver().statement_activity,
            [con]
        )
