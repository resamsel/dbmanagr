#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import expanduser

def get_version():
    """
    Gets the latest version number out of the package, saving us from maintaining it in multiple places.
    """
    local_results = {}
    execfile('src/dbnav/version.py', {}, local_results)
    return local_results['__version__']

setup(
    name = "dbnav",
    version = get_version(),
    author = "René Samselnig",
    author_email = "me@resamsel.com",
    description = "The database navigator for the command line",
    keywords = "database navigator exporter grapher postgres sqlite graphviz diff",

    packages = find_packages(
        'src', exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),
    package_dir = { '':'src' },

    test_suite = 'tests.load_suite',

    # dependencies
    install_requires = [
        'sqlalchemy>=0.9.8',
        'psycopg2>=2.5.1',
        'sqlparse>=0.1.13',
        'mysql-python>=1.2.5'
    ],
    
    tests_require = [
        'flake8>=2.2.5',
        'pep8-naming>=0.2.2',
        'flake8-todo>=0.3'
    ],

    entry_points = {
        'console_scripts': [
            'dbnav = dbnav.navigator:main',
            'dbexport = dbnav.exporter:main',
            'dbgraph = dbnav.grapher:main',
            'dbexec = dbnav.executer:main',
            'dbdiff = dbnav.differ:main'
        ]
    },
    
    data_files = [
        ('/usr/local/etc/bash_completion.d', ['resources/bash_completion/dbnav'])
    ]
)
