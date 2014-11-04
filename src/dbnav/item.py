#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import logging

from dbnav.formatter import Formatter

logger = logging.getLogger(__name__)

def hash(s):
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, s.encode('ascii', 'ignore')))

def item(v):
    if v.__class__.__name__ == 'BaseItem':
        return v.item()
    return v

class Item:
    def __init__(self, value, title, subtitle, autocomplete, valid, icon):
        self.value = value
        self.title = title
        self.subtitle = subtitle
        self.autocomplete = autocomplete
        self.valid = valid
        self.icon = icon
        self.uid = hash(autocomplete)

    def escaped(self, f):
        return dict(map(lambda (k, v): (k.encode('ascii', 'ignore'), f(v)), self.__dict__.iteritems()))

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.title

    def format(self):
        return Formatter.format_item(self)
