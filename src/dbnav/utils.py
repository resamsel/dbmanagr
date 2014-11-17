#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re

from sqlalchemy.types import Integer

from dbnav.logger import LogWith

NAMES = [
    'name', 'title', 'key', 'text', 'username', 'user_name', 'email',
    'comment', 'street', 'city'
]
NAME_SUFFIXES = ['name', 'title', 'key', 'text']

logger = logging.getLogger(__name__)


def prefixes(items):
    return set([re.sub('([^\\.]*)\\..*', '\\1', i) for i in items])


def remove_prefix(prefix, items):
    p = '%s.' % prefix
    return [re.sub('^%s' % p, '', i) for i in items if i.startswith(p)]


def tostring(key):
    if isinstance(key, unicode):
        return key.encode('ascii', errors='ignore')
    return key


def dictsplus(dicts, key, value):
    for d in dicts:
        dictplus(d, key, value)
    return dicts


def dictplus(d, key, value):
    d[key] = value


def dictminus(d, key):
    r = dict(d)
    if key in d:
        del r[key]
    return r


@LogWith(logger)
def create_title(comment, columns):
    # Find certain column names (but their type is not an integer - integers
    # are no good names)
    for c in columns:
        for name in filter(lambda name: c.name == name, NAMES):
            if not isinstance(c.type, Integer):
                return (name, '{%s}' % c.name)

    # Find first column that ends with any of certain suffixes
    for c in columns:
        for name in filter(lambda s: c.name.endswith(s), NAME_SUFFIXES):
            if not isinstance(c.type, Integer):
                return (name, c.name)

    # Use the comment id, if any
    if comment.id:
        return ('{id}', comment.id)

    # Default: use the first column
    return ('First column', columns[0].name)
