#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

def prefixes(items):
    return set([re.sub('([^\\.]*)\\..*', '\\1', i) for i in items])

def remove_prefix(prefix, items):
    p = '%s.' % prefix
    return [re.sub('^%s' % p, '', i) for i in items if i.startswith(p)]

