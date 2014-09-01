#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import logging

from dbnav.formatter import Formatter

VALID = "yes"
INVALID = "no"

logger = logging.getLogger(__name__)

def hash(s):
    #logger.debug('hash(%s)' % s)
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, s.encode('ascii', 'ignore')))

def item(v):
    if v.__class__.__name__ == 'BaseItem':
        return v.item()
    return v

def create_connections(cons):
    """Creates connection items"""

    return map(lambda c: c.item(), cons)

def create_databases(dbs):
    """Creates database items"""

    return map(lambda db: db.item(), dbs)

def create_tables(tables):
    """Creates table items"""

    return map(lambda t: t.item(), tables)

def create_columns(columns):
    """Creates column items"""

    return map(lambda c: c.item(), columns)

def create_rows(rows):
    """Creates row items"""

    return map(Formatter.format_row, rows)

def create_values(values):
    """Creates value items"""

    return map(item, cons)

def create_items(items, options):
    """Creates any items"""
    
    logger.debug('create_items(items=%s, options=%s)', items, options)

    if options.show == 'connections':
        return create_connections(items)

    if options.show == 'databases':
        return create_databases(items)

    if options.show == 'tables':
        return create_tables(items)

    if options.show == 'columns':
        if options.filter == None:
            return create_columns(items)
        else:
            return create_rows(items)
            
    if options.show == 'values':
        return create_values(items)

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
