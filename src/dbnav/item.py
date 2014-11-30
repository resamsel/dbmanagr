#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from dbnav.utils import hash
from dbnav.formatter import Formatter

logger = logging.getLogger(__name__)


def item(v):
    if v.__class__.__name__ == 'BaseItem':
        return v.item()
    return v


class Item:
    def __init__(self, value, title, subtitle, autocomplete, validity, icon):
        self.value = value
        self.title = title
        self.subtitle = subtitle
        self.autocomplete = autocomplete
        self.validity = validity
        self.icon = icon
        self.uid = hash(autocomplete)

    def escaped(self, f):
        return dict(map(
            lambda (k, v): (k.encode('ascii', 'ignore'), f(v)),
            self.__dict__.iteritems()))

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.title

    def format(self):
        return Formatter.format_item(self)
