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

from os import path

from sqlalchemy.exc import OperationalError

from tests.testcase import DbTestCase
from dbnav.driver import postgresql
from dbnav.driver.postgresql import databaseconnection as dbc
from dbnav.config import Config
from dbnav import navigator
from tests.mock.sources import DIR as MOCK_DIR
from tests.mock.sources import URI as MOCK_URI


class Opts:
    def __init__(self, user=None, password=None, host=None, gen=None):
        self.user = user
        self.password = password
        self.host = host
        self.gen = gen


class DatabaseConnectionTestCase(DbTestCase):
    def test_init(self):
        """Tests the init function"""

        driver, postgresql.DRIVERS = postgresql.DRIVERS, {}
        self.assertIsNone(
            postgresql.init()
        )
        postgresql.DRIVERS = driver

    def test_autocomplete(self):
        """Tests the autocomplete function"""

        self.assertEqual(
            'user@host/db/',
            dbc.PostgreSQLConnection(
                'uri', 'host', '3333', 'db', 'user', 'password'
            ).autocomplete())
        self.assertEqual(
            'user@host/',
            dbc.PostgreSQLConnection(
                'uri', 'host', '3333', None, 'user', 'password'
            ).autocomplete())

    def test_title(self):
        """Tests the title function"""

        self.assertEqual(
            'user@host/db/',
            dbc.PostgreSQLConnection(
                'uri', 'host', '3333', 'db', 'user', 'password'
            ).title())

    def test_subtitle(self):
        """Tests the subtitle function"""

        self.assertEqual(
            'PostgreSQL Connection',
            dbc.PostgreSQLConnection(
                'uri', 'host', '3333', 'db', 'user', 'password'
            ).subtitle())

    def test_filter(self):
        """Tests the filter function"""

        self.assertEqual(
            True,
            dbc.PostgreSQLConnection(
                'uri', 'host', '3333', 'db', 'user', 'password'
            ).filter(Config.init(['user@host/db/'], navigator.args.parser)))
        self.assertEqual(
            False,
            dbc.PostgreSQLConnection(
                'postgresql://{user}:{password}@{host}/{database}',
                'host', '3333', 'db', 'user', 'password'
            ).filter({'postgresql': Opts(user='foo', host=None)}))

    def test_connect(self):
        """Tests the connect function"""

        self.assertRaises(
            OperationalError,
            dbc.PostgreSQLConnection(
                'postgresql://{user}:{password}@{host}/{database}',
                'host', '3333', 'db', 'user', 'password'
            ).connect,
            [None])
        self.assertEqual(
            None,
            dbc.PostgreSQLConnection(
                MOCK_URI.format(
                    file=path.join(MOCK_DIR, '../resources/dbnav.sqlite')),
                'host', '3333', 'db', 'user', 'password'
            ).connect(None))
        self.assertEqual(
            None,
            dbc.PostgreSQLConnection(
                MOCK_URI.format(
                    file=path.join(MOCK_DIR, '../resources/dbnav.sqlite')),
                'host', '3333', 'db', 'user', 'password'
            ).connect(None))
        self.assertEqual(
            None,
            dbc.PostgreSQLConnection(
                MOCK_URI.format(
                    file=path.join(
                        MOCK_DIR, '../resources/dbnav.sqlite')),
                'host', '3333', 'db', 'user', 'password'
            ).connect('db'))
        self.assertEqual(
            None,
            dbc.PostgreSQLConnection(
                MOCK_URI.format(
                    file=path.join(
                        MOCK_DIR, '../resources/{database}/dbnav.sqlite')),
                'host', '3333', 'db', 'user', 'password'
            ).connect('db'))

    def test_databases(self):
        """Tests the databases function"""

        con = dbc.PostgreSQLConnection(
            'postgresql://{user}:{password}@{host}/{database}',
            'host', '3333', 'db', 'user', 'password'
        )

        self.assertRaises(
            Exception,
            con.databases)

        con._databases = []
        self.assertEqual(
            [],
            con.databases())

    def test_init_tables(self):
        """Tests the init_tables method"""

        self.assertRaises(
            Exception,
            dbc.PostgreSQLConnection(
                'postgresql://{user}:{password}@{host}/{database}',
                'host', '3333', 'db', 'user', 'password'
            ).init_tables,
            [None])

    def test_matches(self):
        """Tests the matches method"""

        self.assertEqual(
            False,
            dbc.PostgreSQLConnection(
                'postgresql://{user}:{password}@{host}/{database}',
                'host', '3333', 'db', 'user', 'password'
            ).matches({'postgresql': Opts(gen='foo@bar')}))

    def test_postgresql_database(self):
        """Tests instantiating the PostgreSQLDatabase"""

        con = dbc.PostgreSQLConnection(
            'postgresql://{user}:{password}@{host}/{database}',
            'host', '3333', 'db', 'user', 'password'
        )

        self.assertEqual(
            'user@host/db/',
            dbc.PostgreSQLDatabase(con, 'db').autocomplete())
