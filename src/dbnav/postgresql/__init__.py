#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["databaseconnection", "sources", "options"]

from os.path import expanduser
from os import getenv
from collections import OrderedDict

from dbnav import __drivers__
from dbnav.utils import module_installed
from dbnav.sources import Source
from .sources import PgpassSource, DBExplorerPostgreSQLSource
from dbnav.options import Options
from .options import PostgreSQLOptionsParser

DRIVERS = OrderedDict([
    ('psycopg2', 'postgresql+psycopg2://{user}:{password}@{host}/{database}'),
    ('postgresql',
        'postgresql+pypostgresql://{user}:{password}@{host}/{database}'),
    ('pg8000', 'postgresql+pg8000://{user}:{password}@{host}/{database}'),
    # ('zxjdbc', 'postgresql+zxjdbc://{user}:{password}@{host}/{database}')
])


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

    __drivers__.append(module)
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
