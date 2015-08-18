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

import sys
import logging
import yaml

from dbnav.wrapper import Wrapper
from dbnav.config import Config
from dbnav.logger import LogWith
from dbnav.writer import Writer

from .args import parser
from .writer import ArgumentWriter

logger = logging.getLogger(__name__)


@LogWith(logger)
def consume(tree, parent, includes, excludes, substitutes):
    if (type(tree) is dict and 'includes' in tree
            and type(tree['includes']) is dict):
        dfsi(tree['includes'], parent, includes)
    if (type(tree) is dict and 'excludes' in tree
            and type(tree['excludes']) is dict):
        dfsx(tree['excludes'], parent, excludes)
    if (type(tree) is dict and 'substitutes' in tree
            and type(tree['substitutes']) is dict):
        dfss(tree['substitutes'], parent, substitutes)


def dfsi(tree, parent, includes):
    """Depth first search for includes"""

    for (k, v) in tree.iteritems():
        ref = to_ref(parent, k)
        includes.append(to_forward_ref(ref))
        if type(v) is dict:
            dfsi(v, ref, includes)


def dfsx(tree, parent, excludes):
    """Depth first search for excludes"""

    for (k, v) in tree.iteritems():
        ref = to_ref(parent, k)
        if type(v) is dict:
            dfsx(v, ref, excludes)
        else:
            excludes.append(ref)


def dfss(tree, parent, substitutes):
    """Depth first search for substitutes"""

    for (k, v) in tree.iteritems():
        ref = to_ref(parent, k)
        if type(v) is dict:
            dfss(v, ref, substitutes)
        else:
            substitutes.append('{0}={1}'.format(ref, v))


def to_ref(parent, key):
    if parent is None:
        return key
    return '{0}.{1}'.format(parent, key)


def to_forward_ref(ref):
    if ref.endswith('*'):
        return ref
    return '{0}.'.format(ref)


class DatabaseArgumentor(Wrapper):
    """The main class"""
    def __init__(self, options):
        Wrapper.__init__(self, options)

        if options.formatter:
            Writer.set(options.formatter(options))
        else:
            Writer.set(ArgumentWriter(options))

    @LogWith(logger)
    def execute(self):
        """The main method that splits the arguments and starts the magic"""
        options = self.options

        config = yaml.safe_load(options.infile)

        includes = []
        excludes = []
        substitutes = []

        consume(config, None, includes, excludes, substitutes)

        return (includes, excludes, substitutes)


def execute(args):
    """
    Directly calls the execute method and avoids using the wrapper
    """
    return DatabaseArgumentor(Config.init(args, parser)).execute()


def run(args):
    return DatabaseArgumentor(Config.init(args, parser)).run()


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    return DatabaseArgumentor(Config.init(args, parser)).write()
