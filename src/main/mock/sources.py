#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..sources import *
from .databaseconnection import *

class MockSource(Source):
    def list(self):
        if not self.connections:
            self.connections.append(MockConnection('localhost', '1234', 'mockdb', 'mockuser', 'mockpass'))

        return self.connections
