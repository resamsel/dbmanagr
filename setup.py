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
    execfile('src/dbmanagr/version.py', {}, local_results)
    return local_results['__version__']

setup(
    name="dbmanagr",
    version=get_version(),
    description="The database manager for the command line",
    url="https://github.com/resamsel/dbmanagr",
    author="René Samselnig",
    author_email="me@resamsel.com",
    license="GPLv3+",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 2 :: Only',
        'Topic :: Database',
        'Topic :: Database :: Front-Ends',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],
    keywords="database navigator exporter grapher postgres sqlite graphviz"
             " diff",

    packages=find_packages(
        'src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    package_dir={'': 'src'},

    test_suite='tests',

    # dependencies
    install_requires=[
        'sqlalchemy==0.9.10',
        'sqlparse>=0.1.13',
        'ijson>=2.0',
        'pyyaml>=3.11',
        # 'psycopg2>=2.5.1',
        # 'mysql-python>=1.2.5'
    ],

    tests_require=[
        'flake8>=2.2.5',
        'pep8-naming>=0.2.2',
        'flake8-todo>=0.3',
        'nose>=1.3.4',
        'coverage>=3.7.1',
        'pylint>=1.4.3',
        'pg8000>=1.08',
        'pymysql>=0.6.2',
    ],

    entry_points={
        'console_scripts': [
            'dbnav = dbmanagr.command.navigator:main',
            'dbexport = dbmanagr.command.exporter:main',
            'dbgraph = dbmanagr.command.grapher:main',
            'dbexec = dbmanagr.command.executer:main',
            'dbdiff = dbmanagr.command.differ:main',
            'dbdaemon = dbmanagr.command.daemon:main',
            'dbstac = dbmanagr.command.activity:main',
            'dbargs = dbmanagr.command.argumentor:main',
        ]
    },

    data_files=[
#        (
#            '/usr/local/etc/bash_completion.d',
#            ['resources/bash_completion/dbmanagr']
#        )
    ]
)
