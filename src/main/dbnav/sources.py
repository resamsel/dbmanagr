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
            logger.debug('class(source): %s, class(source.list()): %s', source.__class__.__name__, source.list().__class__.__name__)
            cons += source.list()
        return set(cons)
