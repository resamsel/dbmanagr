#!/usr/bin/env python
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
from workflow import Workflow

__version__ = "0.22.0"

def main(wf):
    from dbnav.command import navigator

    wf.logger.debug('Args: %s', wf.args)

    items = navigator.run(wf.args)
    
    for item in items:
        wf.add_item(
            unicode(item.title()),
            unicode(item.subtitle()),
            uid=item.uid(),
            arg=unicode(item.value()),
            autocomplete=item.autocomplete(),
            valid=item.validity(),
            icon=item.icon())

    # Send output to Alfred
    wf.send_feedback()

if __name__ == '__main__':
    wf = Workflow(
        libraries=[
            'lib/dbnav-{}-py2.7.egg'.format(__version__),
            'lib/ijson-2.0-py2.7.egg',
            'lib/SQLAlchemy-0.9.8-py2.7-macosx-10.10-x86_64.egg',
            'lib/pg8000-1.10.1-py2.7.egg',
            'lib/PyMySQL3-0.5-py2.7.egg'
        ],
        update_settings={
            'github_slug': 'resamsel/dbnavigator',
            'version': __version__
        })
    sys.exit(wf.run(main))
