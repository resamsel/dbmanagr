# -*- coding: utf-8 -*-
#
# Copyright © 2014 René Samselnig
#
# This file is part of Database Navigator.
#
# Database Navigator is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Database Navigator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Database Navigator.  If not, see <http://www.gnu.org/licenses/>.
#

import logging
import re
import pkgutil
import os
import sys
import uuid

from sqlalchemy.sql.sqltypes import Boolean, Integer, Float, String, \
    Date, Time, DateTime, _Binary

# from dbmanagr.logger import LogWith

NAMES = [
    'name', 'title', 'key', 'text', 'first_name', 'username', 'user_name',
    'last_name', 'email', 'comment', 'street', 'city'
]
NAME_SUFFIXES = ['name', 'title', 'key', 'text']

logger = logging.getLogger(__name__)


def hash_(s):
    try:
        return str(uuid.uuid3(uuid.NAMESPACE_DNS, s.encode('ascii', 'ignore')))
    except:
        return hash(s)


def module_installed(*modules):
    installed = map(lambda m: m[1], pkgutil.iter_modules())
    for module in modules:
        if module in installed:
            return module
    return None


def prefix(item, separator='\\.'):
    return re.sub('([^{0}]*){0}.*'.format(separator), '\\1', item)


def prefixes(items):
    if items is None:
        return None

    if type(items) is dict:
        return dict(filter(
            lambda (k, v): len(prefix(k)), map(
                lambda (k, v): (prefix(k), v),
                filter(
                    lambda (k, v): '.' not in k,
                    items.iteritems())
                )
        ))

    return set(filter(len, map(prefix, items)))


def remove_prefix(prefix, items):
    if items is None:
        return None

    p = '%s.' % prefix

    if type(items) is dict:
        return dict(map(
            lambda (k, v): (re.sub('^%s' % p, '', k), v),
            filter(
                lambda (k, v): k.startswith(p),
                items.iteritems())
        ))

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


def is_name(name):
    return lambda c: c.name == name


def ends_with(suffix):
    return lambda c: c.name.endswith(suffix)


# @LogWith(logger)
def create_title(comment, columns, exclude=None):
    if exclude is None:
        exclude = []

    # Find certain column names (but their type is not an integer - integers
    # are no good names)
    for name in filter(lambda n: n not in exclude, NAMES):
        for c in filter(is_name(name), columns):
            if not isinstance(c.type, Integer):
                return (name, '{%s}' % c.name)

    # Find first column that ends with any of certain suffixes
    for suffix in filter(lambda n: n not in exclude, NAME_SUFFIXES):
        for c in filter(ends_with(suffix), columns):
            if not isinstance(c.type, Integer):
                return (c.name, '{%s}' % c.name)

    # Use the comment id, if any
    if comment and comment.id:
        return ('id', '{%s}' % comment.id)

    # Default: use the first column
    if len(columns) > 0:
        return (columns[0].name, '{%s}' % columns[0].name)

    return (None, None)


# @LogWith(logger)
def foreign_key_or_column(table, column):
    fk = table.foreign_key(column)
    if fk:
        return fk
    return table.column(column)


def operation(column, operator, value):
    from dbmanagr import OPERATORS
    return OPERATORS.get(operator)(column, value)


def unicode_decode(arg):
    if type(arg) is list:
        return map(unicode_decode, arg)
    if type(arg) is unicode:
        return arg
    if type(arg) in [int, bool, float]:
        return unicode(arg)
    return arg.decode('utf-8')


def mute_stderr(f):
    def wrapper(*args, **kwargs):
        devnull = open(os.devnull, 'w')
        stderr, sys.stderr = sys.stderr, devnull
        try:
            return f(*args, **kwargs)
        finally:
            sys.stderr.close()
            sys.stderr = stderr

    return wrapper


def matches(name, patterns):
    for pattern in patterns:
        p = re.compile(replace_wildcards(pattern))
        if p.match(name):
            return True

    return False


def replace_wildcards(pattern):
    if not pattern:
        return pattern

    return pattern.replace('*', '.*')


def primary_key_or_first_column(table):
    column = table.primary_key
    if not column:
        column = table.column(0).name
    return column


def filter_keys(d, *keys):
    return dict(filter(lambda (k, v): k in keys, d.iteritems()))


def freeze(d):
    if isinstance(d, dict):
        return frozenset((key, freeze(value)) for key, value in d.items())
    elif isinstance(d, list):
        return tuple(freeze(value) for value in d)
    return d


def escape_statement(stmt):
    """Escapes the given statement for use with SQLAlchemy"""

    return stmt.replace('%', '%%')


def find_connection(cons, options, matcher):
    logger.debug(
        'find_connection(cons=%s, options=%s, matcher=%s)',
        cons, options, matcher)
    for con in cons:
        opts = options.get(con.dbms)
        logger.debug('matcher(con=%s, opts=%s)', con, opts)
        if matcher(con, opts):
            return (con, opts)

    return (None, None)


def to_dict(opts, d=None):
    """
    Creates a dictionary from the given list of strings. The dict keys are
    separated by dots. This can be used to create the includes/excludes/
    substitutes given as command line arguments.
    """

    if d is None:
        d = {}
    if opts is None:
        return d

    for opt in opts:
        s = opt.split('=', 1)
        key = s[0]
        val = None
        if len(s) > 1:
            val = s[1]

        if key == '':
            if d == {}:
                # Overwrite newly created dict
                d = None
            return d

        if '.' in key:
            # Recurse into keys
            pfx = prefix(key)
            if pfx not in d or type(d[pfx]) is bool:
                d[pfx] = {}
            d[pfx] = to_dict(remove_prefix(pfx, [opt]), d[pfx])
        else:
            d[prefix(key)] = val

    return d


# Example
#
# a:
#   b: False
#   c: True
# d:
# e:
#   f:
#     g:
#
# When Included: a, a.c, d, e, e.f, e.f.g
# When Excluded: a.c, d, e.f.g
#
def is_included(name, d):
    """Checks the given content selection dict for inclusion of name"""

    if d is None:
        # None means included
        return True
    if d is False:
        return False
    # Type must be dict, then any value (None, dict, True) except for False
    # includes name
    if type(d) is dict:
        if '*' in d:
            # Wildcard matches any element within this level
            return True
        return d.get(name, False) is not False
    return False


def is_excluded(name, d):
    """Checks the given content selection dict for exclusion of name"""

    if d is None:
        # None means excluded
        return True
    if d is False:
        return False
    if type(d) is dict:
        if '*' in d:
            # Wildcard matches any element within this level
            return True
        val = d.get(name, True)
        return val is None or val is False
    return True


def selection(name, d):
    """Retrieves the content selection for the given name"""

    if type(d) is dict:
        return d.get(name, False)
    return False


def is_node(tree, name):
    """Checks whether the name is part of the tree dict"""

    return (
        type(tree) is dict
        and name in tree
        and type(tree[name]) is dict)


def to_ref(parent, key):
    if parent is None:
        return key
    return '{0}.{1}'.format(parent, key)


def to_forward_ref(ref):
    if ref.endswith('*'):
        return ref
    return '{0}.'.format(ref)


def to_yaml_type(type_):
    if isinstance(type_, Integer):
        return 'int'
    if isinstance(type_, Float):
        return 'float'
    if isinstance(type_, String):
        return 'str'
    if isinstance(type_, Boolean):
        return 'bool'
    if (isinstance(type_, DateTime)
            or isinstance(type_, Date)
            or isinstance(type_, Time)):
        return 'str'
    if isinstance(type_, _Binary):
        return 'binary'
    return 'str'


def shell_escape(s):
    if type(s) in (str, unicode):
        if "'" in s:
            return u'"{0}"'.format(s)
        return u"'{0}'".format(s)
    return unicode(s)
