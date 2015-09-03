#!/bin/bash

THEAD=$(cat <<EOF
Title | Subtitle
----- | --------
EOF
)

cat <<EOF > README.md
# Database Navigator

[![Build Status](https://api.travis-ci.org/resamsel/dbnavigator.svg)](https://travis-ci.org/resamsel/dbnavigator)
[![Coverage Status](https://coveralls.io/repos/resamsel/dbnavigator/badge.svg?branch=master&service=github)](https://coveralls.io/github/resamsel/dbnavigator?branch=master)

Allows you to explore, visualise, and export your database recursively. Additionally allows to explore the database using the Powerpack of Alfred 2.0.

![Database Grapher Example](resources/images/dbgraph-example.png "Database Grapher Example")

[TOC]

## Main Features
* Database Navigation
* Database Visualisation
* Database Export
* Database Execution
* Database Diff
* Supported databases: PostgreSQL, MySQL, SQLite
* Use database connection definitions from
  * the \`~/.pgpass\` configuration file (PGAdmin)
  * the \`~/.mypass\` configuration file (like \`~/.pgpass\`)
  * the \`~/.dbexplorer/dbexplorer.cfg\` configuration file (DBExplorer)
  * the Navicat configuration file (SQLite)

## Database Navigation

Documentation: [Navigator wiki page](https://github.com/resamsel/dbnavigator/wiki/Navigator)

### Features

* Shows databases of configured connections
* Shows tables of databases
* Shows columns of tables for restricting rows
* Shows rows of tables with multiple restrictions (operators: =, !=, >, <, >=, <=, like, in)
* Shows detailed row information
* Shows info of foreign table row (based on the foreign key)
* Switch to the foreign table row (forward references)
* Shows foreign keys that point to the current table row (back references)
* Configuration of what is shown based on table comments (currently PostgreSQL only)

## Database Visualisation

Visualises the dependencies of a table using its foreign key references (forward and back references).

Documentation: [Grapher wiki page](https://github.com/resamsel/dbnavigator/wiki/Grapher)

### Features
* Optionally display columns as well as references
* Highlights primary keys (*) and optional columns (?)
* Optionally include or exclude columns/dependencies from the graph
* Optionally enable recursive inclusion (outputs each table only once, so cycles are not an issue)
* Ouput formats include hierarchical text and a Graphviz directed graph
* Uses the same configuration and URI patterns as the Database Navigator

## Database Exporter

Exports specific rows from the database along with their references rows from other tables.

Documentation: [Exporter wiki page](https://github.com/resamsel/dbnavigator/wiki/Exporter)

### Features
* Exports the rows matching the given URI as SQL insert statements
* Allows inclusion of referenced tables (forward and back references)
* Allows exclusion of specific columns (useful if columns are optional, or cyclic references exist)
* Takes into account the ordering of the statements (when table A references table B, then the referenced row from B must be inserted first)
* Limits the number of returned rows of the main query (does not limit referenced rows)

## Database Executer

Executes the SQL statements from the given file on the database specified by the given URI.

Documentation: [Executer wiki page](https://github.com/resamsel/dbnavigator/wiki/Executer)

## Database Differ

A diff tool that compares the structure of two database tables with each other.

Documentation: [Differ wiki page](https://github.com/resamsel/dbnavigator/wiki/Differ)

## Installation

Installing using PIP also upgrades to the latest version:

\`\`\`
sudo pip install --upgrade git+https://github.com/resamsel/dbnavigator.git#egg=dbnav
\`\`\`

You might want to install database drivers for PostgreSQL and MySQL as well:

\`\`\`
sudo pip install pg8000 pymysql
\`\`\`

More information and installation options can be found on the [Installation wiki page](https://github.com/resamsel/dbnavigator/wiki/Installation).

## Configuration

Configuration of *connections* is described in the [Connection Configuration wiki page](https://github.com/resamsel/dbnavigator/wiki/Connection-Configuration).

Configuration of *content* is described in the [Content Configuration wiki page](https://github.com/resamsel/dbnavigator/wiki/Content-Configuration).

## Development

More information can be found on the [Development wiki page](https://github.com/resamsel/dbnavigator/wiki/Development).

EOF
