#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources"]

from os.path import expanduser
from os import getenv

from ..sources import Source
from .sources import *
from ..options import Options
from .options import *

Source.sources.append(DBExplorerPostgreSQLSource(getenv('DBEXPLORER_CFG',
     expanduser('~/.dbexplorer/dbexplorer.cfg'))))
Source.sources.append(PgpassSource(getenv('PGPASS_CFG',
    expanduser('~/.pgpass'))))
# Doesn't make much sense at the moment - passwords are encrypted in the plist file
#Source.sources.append(NavicatPostgreSQLSource(getenv('NAVICAT_CFG',
#    expanduser('~/Library/Application Support/PremiumSoft CyberTech/preference.plist'))))

Options.parser['postgresql'] = PostgreSQLOptions()
