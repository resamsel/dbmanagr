#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ["sources"]

from dbnav.sources import Source
from .sources import MockSource


def init_mock():
    Source.sources.append(MockSource())
