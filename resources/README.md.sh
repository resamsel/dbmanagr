#!/bin/bash

THEAD=$(cat <<EOF
Title | Subtitle
----- | --------
EOF
)

cat <<EOF > README.md
# Database Navigator

Allows you to explore, visualise and export your database. Additionally allows to explore the database using the Powerpack of Alfred 2.0.

![Alfred Database Navigator Sample](resources/images/dbnav-example.png "Alfred Database Navigator Sample")

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

### Usage
\`\`\`
`dbnav -h`
\`\`\`

In Alfred the keyword is *dbnav*. The query after the keyword is the URI to your data. No options may be given.

### Examples

#### Show Available Connections
\`dbnav\`

#### Show Databases of Connection
\`dbnav myuser@myhost/\`

#### Show Tables of Database
\`dbnav dbnav.sqlite/\`

$THEAD
`dbnav dbnav.sqlite/ | sed 's/	/ | /g'`

#### Show Columns of Table
\`dbnav dbnav.sqlite/user?\`

$THEAD
`dbnav dbnav.sqlite/user? | sed 's/	/ | /g'`

#### Show Rows where Column equals Value
\`dbnav dbnav.sqlite/user?first_name=Joshua\`

$THEAD
`dbnav dbnav.sqlite/user?first_name=Joshua | sed 's/	/ | /g'`

#### Show Rows where multiple Columns equals Value
When using the ampersand (&) in a shell make sure to escape it (prepend it with a backslash (\) in Bash), since it has a special meaning there.

\`dbnav dbnav.sqlite/user?first_name=Joshua&last_name=Alexander\`

$THEAD
`dbnav dbnav.sqlite/user?first_name=Joshua\&last_name=Alexander | sed 's/	/ | /g'`

#### Show Rows where Column matches Pattern
The tilde (~) will be translated to the *like* operator in SQL. Use the percent wildcard (%) to match arbitrary strings.

\`dbnav dbnav.sqlite/user?first_name~%osh%\`

$THEAD
`dbnav dbnav.sqlite/user?first_name~%osh% | sed 's/	/ | /g'`

#### Show Rows where Column is in List
The colon (:) will be translated to the *in* operator in SQL.

\`dbnav dbnav.sqlite/user?first_name:Herbert,Josh,Martin\`

$THEAD
`dbnav dbnav.sqlite/user?first_name:Herbert,Josh,Martin | sed 's/	/ | /g'`

#### Show Rows where any (Search) Column matches Pattern
\`dbnav myuser@myhost/mydatabase/mytable?~%erber%\`

**Warning: this is a potentially slow query! See configuration for options to resolve this problem.**

#### Show Values of selected Row
\`dbnav dbnav.sqlite/user/?id=2\`

$THEAD
`dbnav dbnav.sqlite/user/?id=2 | sed 's/	/ | /g'`

## Database Visualisation
Visualises the dependencies of a table using its foreign key references (forward and back references).

### Features
* Optionally display columns as well as references
* Highlights primary keys (*) and optional columns (?)
* Optionally include or exclude columns/dependencies from the graph
* Optionally enable recursive inclusion (outputs each table only once, so cycles are not an issue)
* Ouput formats include hierarchical text and a Graphviz directed graph
* Uses the same configuration and URI patterns as the Database Navigator

### Usage
\`\`\`
`dbgraph -h`
\`\`\`

### Examples

#### Show references of table
\`dbgraph dbnav.sqlite/article\`

\`\`\`
`dbgraph dbnav.sqlite/article`
\`\`\`

#### Show References and Columns
\`dbgraph -c dbnav.sqlite/article\`

\`\`\`
`dbgraph -c dbnav.sqlite/article`
\`\`\`

#### Show all References recursively
\`dbgraph -r dbnav.sqlite/article\`

\`\`\`
`dbgraph -r dbnav.sqlite/article`
\`\`\`

#### Show specific References
\`dbgraph -i user_id.blog_user dbnav.sqlite/article\`

\`\`\`
`dbgraph -i user_id.blog_user dbnav.sqlite/article`
\`\`\`

#### Show specific References and exclude others
\`dbgraph -i user_id.blog_user -x user_id.blog_user.user_id dbnav.sqlite/article\`

\`\`\`
`dbgraph -i user_id.blog_user -x user_id.blog_user.user_id dbnav.sqlite/article`
\`\`\`

#### Show specific References as Graphviz Graph
\`dbgraph -G -i user_id dbnav.sqlite/article\`

\`\`\`
`dbgraph -G -i user_id dbnav.sqlite/article`
\`\`\`

## Database Exporter
Exports specific rows from the database along with their references rows from other tables.

### Features
* Exports the rows matching the given URI as SQL insert statements
* Allows inclusion of referenced tables (forward and back references)
* Allows exclusion of specific columns (useful if columns are optional, or cyclic references exist)
* Takes into account the ordering of the statements (when table A references table B, then the referenced row from B must be inserted first)
* Limits the number of returned rows of the main query (does not limit referenced rows)

### Usage
\`\`\`
`dbexport -h`
\`\`\`

### Examples

#### Export Contents of Table
\`dbexport dbnav.sqlite/article?id=2\`

\`\`\`
`dbexport dbnav.sqlite/article?id=2`
\`\`\`

#### Export limited Contents of Table
\`dbexport -m 1 dbnav.sqlite/article?*\`

\`\`\`
`dbexport -m 1 dbnav.sqlite/article?*`
\`\`\`

#### Export Contents of Table with Specific References
\`dbexport -i user_id dbnav.sqlite/article?id=2\`

\`\`\`
`dbexport -i user_id dbnav.sqlite/article?id=2`
\`\`\`

#### Export Contents of Table with Specific References and exclude columns
\`dbexport -i user_id -x user_id.url,text dbnav.sqlite/article?id=2\`

\`\`\`
`dbexport -i user_id -x user_id.url,text dbnav.sqlite/article?id=2`
\`\`\`

#### Export Contents of Table as Update Statements
\`dbexport -U dbnav.sqlite/article?id=2\`

\`\`\`
`dbexport -U dbnav.sqlite/article?id=2`
\`\`\`

#### Export Contents of Table as Delete Statements
\`dbexport -D dbnav.sqlite/article?id=2\`

\`\`\`
`dbexport -D dbnav.sqlite/article?id=2`
\`\`\`

#### Export Contents of Table as YAML
\`dbexport -Y dbnav.sqlite/article?id=2 -p my.models\`

\`\`\`
`dbexport -Y dbnav.sqlite/article?id=2 -p my.models`
\`\`\`

## Database Executer
Executes the SQL statements from the given file on the database specified by the given URI.

### Usage
\`\`\`
`dbexec -h`
\`\`\`

## Database Differ
A diff tool that compares the structure of two database tables with each other.

### Usage
\`\`\`
`dbdiff -h`
\`\`\`

### Examples

#### Diff two Tables
\`dbdiff dbnav.sqlite/user dbnav.sqlite/user2\`

\`\`\`
`dbdiff dbnav.sqlite/user dbnav.sqlite/user2`
\`\`\`

#### Diff two Tables Side-by-Side
\`dbdiff -S dbnav.sqlite/user dbnav.sqlite/user2\`

\`\`\`
`dbdiff -S dbnav.sqlite/user dbnav.sqlite/user2`
\`\`\`

#### Diff two Tables Side-by-Side using Column Definitions
\`dbdiff -Sc dbnav.sqlite/user dbnav.sqlite/user2\`

\`\`\`
`dbdiff -Sc dbnav.sqlite/user dbnav.sqlite/user2`
\`\`\`

## Installation
Install the [latest egg-file](dist/dbnav-`python src/dbnav/version.py`-py2.7.egg?raw=true) from the dist directory.

\`\`\`
pip install dbnav-`python src/dbnav/version.py`-py2.7.egg
\`\`\`

### Alfred Workflow
To install the Alfred workflow open the [Database Navigator.alfredworkflow](dist/Database Navigator.alfredworkflow?raw=true) file from the dist directory.

## Connection Configuration
To be able to connect to a certain database you’ll need the credentials for that database. Such a connection may be added with PGAdmin (which puts it into the ~/.pgpass file) or added directly into the ~/.pgpass file.

### Sample ~/.pgpass
The ~/.pgpass file contains a connection description per line. The content of that file might look like this:

\`\`\`
dbhost1:dbport:*:dbuser1:dbpass1
dbhost2:dbport:*:dbuser2:dbpass2
\`\`\`

## Content Configuration
It's possible to configure the content of the result items for the Database Navigation. The configuration is placed as a table comment (currently PostgreSQL only). This is mostly helpful for displaying results in Alfred, but may come in handy for the command line tools as well.

### Usage
\`\`\`
{
  "title": "{fname} {lname}",
  "subtitle": "{email} ({user_name})",
  "search": ["email", "user_name"],
  "display": ["fname", "lname", "email", "user_name", "security_info_id", "staff", "disqualified", "time_zone_id", "address", "id"],
  "order": ["fname", "lname"]
}
\`\`\`
### Title
The *title* is the main entry within the Alfred result item. The string *{0}* will be replaced with the table alias (useful when joining with other tables that also have the given attribute present). The replaced content will then be added to the projection list as is (SQL functions may be added as well as string concatenation as in the example above).

### Subtitle
The *subtitle* is the second line within the Alfred result item. The same replacements as with the title will be applied.

### Search
The *search* array contains the columns that will be looked into when no column is present in the Alfred query. The same replacements as with the title will be applied.

This should be used to speed up the query significantly. When no *search* is configured the generated query will look something like this (see example **Show Rows where any (Search) Column matches Pattern**):

\`\`\`
select
		...
	from mytable
	where
		cast(col1 as text) like '%erber%'
		or cast(col2 as text) like '%erber%'
		...
		or cast(colN as text) like '%erber%'
\`\`\`

When *search* is configured as \`["col1", "col7"]\` the generated query will look more like this:

\`\`\`
select
		...
	from mytable
	where
		cast(col1 as text) like '%erber%'
		or cast(col7 as text) like '%erber%'
\`\`\`

### Display
The *display* array contains the columns that will be added to the projection list of the SQL query. All items present in the projection list will be shown in the *values* view (see example **Show Values of selected Row**). It will be added as is (no replacements will take place).

### Order
The *order* array will be added to the *order by* part of the SQL query. It will be added as is (no replacements will take place).

## Development
If you want to change anything in the source you can build and install the project by using the make command. You’ll probably need to fiddle around with the ALFRED_WORKFLOW Makefile variable, though.

\`\`\`
export ALFRED_WORKFLOW=~/Library/Application Support/Alfred 2/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD
make install
\`\`\`

To simplify development you’d better use \`make develop\` once and have code changes reflected as soon as you save your file. Super easy development powered by [distutils](https://docs.python.org/2/distutils/index.html).

Using distutils you could easily create a Windows binary (\`./setup.py bdist_msi\`) or a Red Hat *rpm* package (\`./setup.py bdist_rpm\`).

EOF