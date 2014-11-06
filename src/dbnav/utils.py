#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re


def encode(v):
    if v is None:
        return None
    if type(v) is unicode:
        return v
    if type(v) is str:
        return unicode(v, 'UTF-8')
    if type(v) is list:
        return map(encode, v)
    return unicode(v)


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
