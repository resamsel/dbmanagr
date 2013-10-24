#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import logging

def hash(s):
#    logging.debug('hash(%s)' % s)
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, s.encode('ascii', 'ignore')))

class Item:
    def __init__(self, title, subtitle, autocomplete, valid, icon):
        self.title = title
        self.subtitle = subtitle
        self.autocomplete = autocomplete
        self.valid = valid
        self.icon = icon
        self.uid = hash(autocomplete)
    def escaped(self, f):
        return dict(map(lambda (k, v): (k, f(v)), self.__dict__.iteritems()))
    def __str__(self):
        return str(self.__dict__)
