#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources", "options"]

from os.path import expanduser
from os import getenv

from dbnav.sources import Source
from .sources import PgpassSource, DBExplorerPostgreSQLSource
from dbnav.options import Options
from .options import PostgreSQLOptionsParser


def init_postgresql(dbexplorer_config, pgpass_config, navicat_config):
    Source.sources.append(DBExplorerPostgreSQLSource(dbexplorer_config))
    Source.sources.append(PgpassSource(pgpass_config))
    # Doesn't make much sense at the moment - passwords are encrypted in the plist file
    # Source.sources.append(NavicatPostgreSQLSource(navicat_config))

init_postgresql(
    getenv('DBEXPLORER_CFG',
        expanduser('~/.dbexplorer/dbexplorer.cfg')),
    getenv('PGPASS_CFG',
        expanduser('~/.pgpass')),
    getenv('NAVICAT_CFG',
        expanduser('~/Library/Application Support/PremiumSoft CyberTech/preference.plist'))
)

Options.parser['postgresql'] = PostgreSQLOptionsParser()
