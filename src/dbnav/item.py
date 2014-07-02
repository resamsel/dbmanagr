#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import logging

logger = logging.getLogger(__name__)

def hash(s):
    #logger.debug('hash(%s)' % s)
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, s.encode('ascii', 'ignore')))

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
