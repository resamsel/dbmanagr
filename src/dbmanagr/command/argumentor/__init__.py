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

from dbmanagr.wrapper import Wrapper
from dbmanagr.config import Config
from dbmanagr.logger import LogWith
from dbmanagr.writer import Writer
from dbmanagr.utils import is_node, to_ref, to_forward_ref, shell_escape

from .args import parser
from .writer import ArgumentWriter

logger = logging.getLogger(__name__)


@LogWith(logger)
def consume(tree, parent, includes, excludes, substitutes):
    if is_node(tree, 'includes'):
        dfs(tree['includes'], parent, includes,
            lambda ref, v: to_forward_ref(ref))
    if is_node(tree, 'excludes'):
        dfs(tree['excludes'], parent, excludes,
            lambda ref, v: ref)
    if is_node(tree, 'substitutes'):
        dfs(tree['substitutes'], parent, substitutes,
            lambda ref, v: u'{0}={1}'.format(ref, shell_escape(v)))


@LogWith(logger)
def dfs(tree, parent, selection, conversion):
    """Depth first search for selection"""

    for (k, v) in tree.iteritems():
        ref = to_ref(parent, k)
        if type(v) is dict:
            dfs(v, ref, selection, conversion)
        else:
            selection.append(conversion(ref, v))


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

        logger.debug('Config file: %s', config)

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
