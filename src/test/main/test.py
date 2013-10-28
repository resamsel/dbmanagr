#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging

from main.dbnavigator import *
from main.sources import *
from main.sqlite.sources import *
from main.postgresql.sources import *

logger = logging.getLogger(__name__)

TEST_DIR = "build/testfiles/resources"

Source.sources = []
Source.sources.append(DBExplorerPostgreSQLSource('%s/dbexplorer.cfg' % TEST_DIR))
Source.sources.append(PgpassSource('%s/pgpass' % TEST_DIR))
Source.sources.append(DBExplorerSQLiteSource('%s/dbexplorer.cfg' % TEST_DIR))

main()
