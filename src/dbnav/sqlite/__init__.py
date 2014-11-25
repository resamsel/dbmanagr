#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources"]

from os.path import expanduser
from os import getenv
from collections import OrderedDict

from dbnav.utils import module_installed
from dbnav.sources import Source
from .sources import DBExplorerSQLiteSource, NavicatSQLiteSource
from dbnav.options import Options
from .options import SQLiteOptionsParser

DRIVERS = OrderedDict([
    ('sqlite3', 'sqlite+pysqlite:///{file}')
])


def init_sqlite(uri, dbexplorer_config, navicat_config1, navicat_config2=None):
    Source.sources.append(DBExplorerSQLiteSource(uri, dbexplorer_config))
    Source.sources.append(NavicatSQLiteSource(uri, navicat_config1))
    if navicat_config2:
        Source.sources.append(NavicatSQLiteSource(uri, navicat_config2))


def init():
    module = module_installed(*DRIVERS.keys())
    if not module:
        return

    init_sqlite(
        DRIVERS[module],
        getenv(
            'DBEXPLORER_CFG',
            expanduser('~/.dbexplorer/dbexplorer.cfg')),
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
