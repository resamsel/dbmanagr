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

__all__ = ["databaseconnection", "driver"]

from os.path import expanduser
from os import getenv
from collections import OrderedDict

from dbmanagr import __drivers__
from dbmanagr.utils import module_installed
from dbmanagr.sources.source import Source
from dbmanagr.sources.dbexplorer import DBExplorerSource
from dbmanagr.sources.anypass import AnyFilePassSource
from dbmanagr.sources.navicat import NavicatSource
from dbmanagr.options import Options
from .databaseconnection import SQLiteConnection
from .driver import SQLiteOptionsParser

DRIVERS = OrderedDict([
    ('sqlite3', 'sqlite+pysqlite:///{file}')
])


def init_sqlite(
        uri,
        dbexplorer_config,
        sqlitepass_config,
        navicat_config1,
        navicat_config2=None):
    Source.sources.append(
        DBExplorerSource(uri, dbexplorer_config, 'sqlite', SQLiteConnection))
    Source.sources.append(
        AnyFilePassSource(uri, sqlitepass_config, SQLiteConnection))
    Source.sources.append(
        NavicatSource(uri, navicat_config1, 'SQLite', SQLiteConnection))
    if navicat_config2:
        Source.sources.append(
            NavicatSource(uri, navicat_config2, 'SQLite', SQLiteConnection))


def init():
    module = module_installed(*DRIVERS.keys())
    if not module:
        return

    __drivers__.append(module)
    init_sqlite(
        DRIVERS[module],
        getenv(
            'DBEXPLORER_CFG',
            expanduser('~/.dbexplorer/dbexplorer.cfg')),
        getenv(
            'SQLITEPASS_CFG',
            expanduser('~/.sqlitepass')),
        getenv(
            'NAVICAT_CFG',
            expanduser('~/Library/Application Support/PremiumSoft CyberTech'
                       '/preference.plist')),
        getenv(
            'NAVICAT_CFG',
            expanduser('~/Library/Containers/com.prect.'
                       'NavicatEssentialsForSQLite/Data/Library/'
                       'Application Support/PremiumSoft CyberTech/'
                       'preference.plist'))
    )

    Options.parser['sqlite'] = SQLiteOptionsParser()
