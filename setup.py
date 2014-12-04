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

from setuptools import setup, find_packages


def get_version():
    """
    Gets the latest version number out of the package, saving us from
    maintaining it in multiple places.
    """
    local_results = {}
    execfile('src/dbnav/version.py', {}, local_results)
    return local_results['__version__']

setup(
    name="dbnav",
    version=get_version(),
    author="René Samselnig",
    author_email="me@resamsel.com",
    description="The database navigator for the command line",
    keywords="database navigator exporter grapher postgres sqlite graphviz"
             " diff",

    packages=find_packages(
        'src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    package_dir={'': 'src'},

    test_suite='tests.load_suite',

    # dependencies
    install_requires=[
        'sqlalchemy>=0.9.8',
        'sqlparse>=0.1.13',
        # 'psycopg2>=2.5.1',
        # 'mysql-python>=1.2.5'
    ],

    tests_require=[
        'flake8>=2.2.5',
        'pep8-naming>=0.2.2',
        'flake8-todo>=0.3'
    ],

    entry_points={
        'console_scripts': [
            'dbnav = dbnav.navigator:main',
            'dbexport = dbnav.exporter:main',
            'dbgraph = dbnav.grapher:main',
            'dbexec = dbnav.executer:main',
            'dbdiff = dbnav.differ:main'
        ]
    },

    data_files=[
        (
            '/usr/local/etc/bash_completion.d',
            ['resources/bash_completion/dbnav']
        )
    ]
)
