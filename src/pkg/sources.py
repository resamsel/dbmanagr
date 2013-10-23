#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
