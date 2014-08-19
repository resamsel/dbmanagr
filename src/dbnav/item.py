#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import logging

VALID = "yes"
INVALID = "no"

logger = logging.getLogger(__name__)

def hash(s):
    #logger.debug('hash(%s)' % s)
    return str(uuid.uuid3(uuid.NAMESPACE_DNS, s.encode('ascii', 'ignore')))

def create_connections(cons):
    """Creates connection items"""

    return [c.item() for c in cons]

def create_databases(dbs):
    """Creates database items"""

    return [database.item() for database in dbs]

def create_tables(tables):
    """Creates table items"""

    return [t.item() for t in tables]

def create_columns(columns):
    """Creates column items"""

    return [c.item() for c in columns]

def create_rows(rows):
    """Creates row items"""

    logger.debug('create_rows(rows=%s)', rows)

    return [row.item() for row in rows]

def create_values(values):
    """Creates value items"""

    logger.debug('create_values(values=%s)', values)

    return [v.item() for v in values]

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
