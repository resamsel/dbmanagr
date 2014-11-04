#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class Source:
    sources = []

    def __init__(self):
        self.connections = []

    def list(self):
        return self.connections

    @staticmethod
    def connections():
        cons = []
        for source in Source.sources:
            cons += source.list()
        return set(cons)

    @staticmethod
    def connection(options):
        # search exact match of connection
        for connection in Source.connections():
            opts = options.get(connection.driver)
            if connection.matches(opts):
                return connection
        return None
