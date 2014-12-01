#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from dbnav.sources import Source
from dbnav.sqlite.databaseconnection import SQLiteConnection

DIR = path.dirname(__file__)
URI = 'sqlite+pysqlite:///{file}'


class MockSource(Source):
    def list(self):
        if not self.connections:
            self.connections.append(
                SQLiteConnection(
                    URI, path.join(DIR, '../resources/dbnav.sqlite')))
            self.connections.append(
                SQLiteConnection(
                    URI, path.join(DIR, '../resources/dbnav-c.sqlite')))
            self.connections.append(
                SQLiteConnection(
                    URI, path.join(DIR, '../resources/me@xyz.com.sqlite')))

        return self.connections
