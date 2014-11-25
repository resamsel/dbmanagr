#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
import pkgutil

from sqlalchemy.types import Integer

from dbnav.logger import LogWith

NAMES = [
    'name', 'title', 'key', 'text', 'first_name', 'username', 'user_name',
    'last_name', 'email', 'comment', 'street', 'city'
]
NAME_SUFFIXES = ['name', 'title', 'key', 'text']

logger = logging.getLogger(__name__)


def module_installed(*modules):
    installed = map(lambda m: m[1], pkgutil.iter_modules())
    for module in modules:
        if module in installed:
            return module
    return None


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
    return d


def dictminus(d, *keys):
    r = dict(d)
    for key in keys:
        if key in d:
            del r[key]
    return r


def getorelse(i, e):
    if i is not None:
        return i
    return e


@LogWith(logger)
def create_title(comment, columns, exclude=None):
    if exclude is None:
        exclude = []

    # Find certain column names (but their type is not an integer - integers
    # are no good names)
    for name in filter(lambda n: n not in exclude, NAMES):
        for c in filter(lambda c: c.name == name, columns):
            if not isinstance(c.type, Integer):
                return (name, '{%s}' % c.name)

    # Find first column that ends with any of certain suffixes
    for suffix in filter(lambda n: n not in exclude, NAME_SUFFIXES):
        for c in filter(lambda c: c.name.endswith(suffix), columns):
            if not isinstance(c.type, Integer):
                return (c.name, '{%s}' % c.name)

    # Use the comment id, if any
    if comment and comment.id:
        return ('id', '{%s}' % comment.id)

    # Default: use the first column
    if len(columns) > 0:
        return (columns[0].name, '{%s}' % columns[0].name)

    return None
