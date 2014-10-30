#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path

from dbnav.sources import Source
from tests.mock import init_mock

def init_sources(dir):
    Source.sources = []
    init_mock()
