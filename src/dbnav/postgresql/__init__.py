#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources", "options"]

from os.path import expanduser
from os import getenv

from dbnav.utils import module_installed
from dbnav.sources import Source
from .sources import PgpassSource, DBExplorerPostgreSQLSource
from dbnav.options import Options
from .options import PostgreSQLOptionsParser

DRIVERS = {
    'psycopg2': 'postgresql'
}


def init_postgresql(driver, dbexplorer_config, pgpass_config, navicat_config):
    Source.sources.append(
        DBExplorerPostgreSQLSource(driver, dbexplorer_config))
    Source.sources.append(
        PgpassSource(driver, pgpass_config))
    # Doesn't make much sense at the moment - passwords are encrypted in the
    # plist file
    # Source.sources.append(NavicatPostgreSQLSource(navicat_config))


def init():
    module = module_installed(*DRIVERS.keys())
    if not module:
        return

    init_postgresql(
        DRIVERS[module],
        getenv(
            'DBEXPLORER_CFG',
            expanduser('~/.dbexplorer/dbexplorer.cfg')),
        getenv(
            'PGPASS_CFG',
            expanduser('~/.pgpass')),
        getenv(
            'NAVICAT_CFG',
            expanduser('~/Library/Application Support/PremiumSoft CyberTech/'
                       'preference.plist'))
    )

    Options.parser['postgresql'] = PostgreSQLOptionsParser()
