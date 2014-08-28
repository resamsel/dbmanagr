#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from dbnav.sources import Source
from dbnav.postgresql import init_postgresql
from dbnav.sqlite import init_sqlite

def init_sources(dir):
    Source.sources = []
    init_postgresql(
        path.join(dir, 'resources/dbexplorer.cfg'),
        path.join(dir, 'resources/pgpass'),
        path.join(dir, 'resources/navicat.plist')
    )
    init_sqlite(
        path.join(dir, 'resources/dbexplorer.cfg'),
        path.join(dir, 'resources/navicat.plist')
    )
