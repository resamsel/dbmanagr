#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources"]

from os.path import expanduser
from os import getenv

from ..sources import Source
from .sources import *
from ..options import Options
from .options import *

def init_sqlite(dbexplorer_config, navicat_config):
    Source.sources.append(DBExplorerSQLiteSource(dbexplorer_config))
    Source.sources.append(NavicatSQLiteSource(navicat_config))

init_sqlite(
    getenv('DBEXPLORER_CFG',
        expanduser('~/.dbexplorer/dbexplorer.cfg')),
    getenv('NAVICAT_CFG',
        expanduser('~/Library/Application Support/PremiumSoft CyberTech/preference.plist'))
)

Options.parser['sqlite'] = SQLiteOptionsParser()
