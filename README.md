# Database Navigator

Allows you to explore, visualise and export your database. Additionally allows to explore the database using the Powerpack of Alfred 2.0.

![Alfred Database Navigator Sample](docs/images/select.png "Alfred Database Navigator Sample")

## Main Features
* Database Navigation
* Database Visualisation
* Database Export
* Supported databases: PostgreSQL, SQLite
* Use database connection definitions from
  * the `~/.pgpass` configuration file (PGAdmin)
  * the `~/.dbexplorer/dbexplorer.cfg` configuration file (DBExplorer)
  * the Navicat configuration file (SQLite)

**Table of Contents**  *generated with [DocToc](http://doctoc.herokuapp.com/)*

- [Database Navigation](#user-content-database-navigation)
	- [Features](#user-content-features)
	- [Usage](#user-content-usage)
	- [Examples](#user-content-examples)
		- [Show Available Connections](#user-content-show-available-connections)
		- [Show Databases of Connection](#user-content-show-databases-of-connection)
		- [Show Tables of Database](#user-content-show-tables-of-database)
		- [Show Columns of Table](#user-content-show-columns-of-table)
		- [Show Rows where Column equals Value](#user-content-show-rows-where-column-equals-value)
		- [Show Rows where Column matches Pattern](#user-content-show-rows-where-column-matches-pattern)
		- [Show Rows where any (Search) Column matches Pattern](#user-content-show-rows-where-any-search-column-matches-pattern)
		- [Show Values of selected Row](#user-content-show-values-of-selected-row)
- [Database Visualisation](#user-content-database-visualisation)
	- [Features](#user-content-features-1)
	- [Usage](#user-content-usage-1)
	- [Examples](#user-content-examples-1)
		- [Show references of table](#user-content-show-references-of-table)
		- [Show References and Columns](#user-content-show-references-and-columns)
		- [Show all References recursively](#user-content-show-all-references-recursively)
		- [Show specific References](#user-content-show-specific-references)
		- [Show specific References and exclude others](#user-content-show-specific-references-and-exclude-others)
		- [Show specific References as Graphviz Graph](#user-content-show-specific-references-as-graphviz-graph)
- [Database Exporter](#user-content-database-exporter)
	- [Features](#user-content-features-1)
	- [Usage](#user-content-usage-2)
- [Database Executer](#user-content-database-executer)
	- [Usage](#user-content-usage-3)
- [Database Differ](#user-content-database-differ)
	- [Usage](#user-content-usage-4)
- [Installation](#user-content-installation)
- [Configuration](#user-content-configuration)
	- [Title](#user-content-title)
	- [Subtitle](#user-content-subtitle)
	- [Search](#user-content-search)
	- [Display](#user-content-display)
	- [Order](#user-content-order)
- [Development](#user-content-development)

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
```
usage: dbnav [-h] [--version] [-f LOGFILE]
             [-l {critical,error,warning,info,debug}] [-T] [-D] [-S] [-J] [-X]
             [-A] [-s] [-N] [-m LIMIT]
             [uri]

A database navigation tool that shows database structure and content

positional arguments:
  uri                   the URI to parse (format for PostgreSQL:
                        user@host/database/table?filter; for SQLite:
                        databasefile.db/table?filter) (default: None)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -s, --simplify        simplify the output (default: True)
  -N, --no-simplify     don't simplify the output (default: True)
  -m LIMIT, --limit LIMIT
                        limit the results of the main query to this amount of
                        rows (default: 50)

logging:
  -f LOGFILE, --logfile LOGFILE
                        the file to log to (default:
                        /usr/local/var/log/dbnav.log)
  -l {critical,error,warning,info,debug}, --loglevel {critical,error,warning,info,debug}
                        the minimum level to log (default: warning)

formatters:
  -T, --test            output format: test specific (default: None)
  -D, --default         output format: default (default: None)
  -S, --simple          output format: simple (default: None)
  -J, --json            output format: JSON (default: None)
  -X, --xml             output format: XML (default: None)
  -A, --autocomplete    output format: autocomplete (default: None)
```

In Alfred the keyword is *dbnav*. The query after the keyword is the URI to your data. No options may be given.

### Examples

#### Show Available Connections
`dbnav`

#### Show Databases of Connection
`dbnav myuser@myhost/`

#### Show Tables of Database
`dbnav dbnav.sqlite/`

```
_comment	Table
address	Table
article	Table
blog	Table
blog_user	Table
sqlite_sequence	Table
user	Table
user_address	Table
```

#### Show Columns of Table
`dbnav dbnav.sqlite/user?`

```
company	user
email	user
first_name	user
gender	user
id	user
last_name	user
phone	user
url	user
username	user
```

#### Show Rows where Column equals Value
`dbnav dbnav.sqlite/user?first_name=Joshua`

```
jalexander80	username (id=289)
jburtonv	username (id=32)
jfernandezc8	username (id=441)
jpalmer8u	username (id=319)
```

#### Show Rows where multiple Columns equals Value
`dbnav dbnav.sqlite/user?first_name=Joshua&last_name=Alexander`

```
jalexander80	username (id=289)
```

When using the ampersand (&) in a shell make sure to escape it (prepend it with a backslash (\) in Bash), since it has a special meaning there.

#### Show Rows where Column matches Pattern
`dbnav dbnav.sqlite/user?first_name~%osh%`

```
jalexander80	username (id=289)
jburtonv	username (id=32)
jfernandezc8	username (id=441)
jpalmer8u	username (id=319)
```

The tilde (~) will be translated to the *like* operator in SQL. Use the percent wildcard (%) to match arbitrary strings.

#### Show Rows where Column is in List
`dbnav dbnav.sqlite/user?first_name:Herbert,Josh,Martin`

```
mdiaze1	username (id=506)
mrichardsonp	username (id=26)
```

The colon (:) will be translated to the *in* operator in SQL.

#### Show Rows where any (Search) Column matches Pattern
`dbnav myuser@myhost/mydatabase/mytable?~%erber%`

**Warning: this is a potentially slow query! See configuration for options to resolve this problem.**

#### Show Values of selected Row
`dbnav dbnav.sqlite/user/?id=2`

```
2	user.id
Evelyn	user.first_name
Gardner	user.last_name
	user.company
egardner1	user.username
	user.email
8-(549)755-1011	user.phone
Female	user.gender
	user.url
← article.user_id	article.user_id
← blog_user.user_id	blog_user.user_id
← user_address.user_id	user_address.user_id
```

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
```
usage: dbgraph [-h] [--version] [-f LOGFILE]
               [-l {critical,error,warning,info,debug}] [-T] [-D] [-G] [-c]
               [-C] [-k] [-K] [-v] [-V] [-n] [-N] [-b] [-B] [-M MAX_DEPTH]
               [-r | -i INCLUDE] [-x EXCLUDE]
               uri

A database visualisation tool that creates graphs from the database structure

positional arguments:
  uri                   the URI to parse (format for PostgreSQL:
                        user@host/database/table; for SQLite:
                        databasefile.db/table)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -c, --columns         include columns in output (default: False)
  -C, --no-columns      don't include columns in output (default: True)
  -k, --back-references
                        include back references in output (default: True)
  -K, --no-back-references
                        don't include back references in output (default:
                        False)
  -v, --driver          include database driver in output (does not work well
                        with graphviz as output) (default: False)
  -V, --no-driver       don't include database driver in output (default:
                        True)
  -n, --connection      include connection in output (does not work well with
                        graphviz as output) (default: False)
  -N, --no-connection   don't include connection in output (default: True)
  -b, --database        include database in output (does not work well with
                        graphviz as output) (default: False)
  -B, --no-database     don't include database in output (default: True)
  -M MAX_DEPTH, --max-depth MAX_DEPTH
                        the maximum depth to use in recursion/inclusion
                        (default: -1)
  -r, --recursive       include any forward/back reference to the starting
                        table, recursing through all tables eventually
                        (default: False)
  -i INCLUDE, --include INCLUDE
                        include the specified columns and their foreign rows,
                        if any. Multiple columns can be specified by
                        separating them with a comma (,) (default: None)
  -x EXCLUDE, --exclude EXCLUDE
                        exclude the specified columns (default: None)

logging:
  -f LOGFILE, --logfile LOGFILE
                        the file to log to (default:
                        /usr/local/var/log/dbnav.log)
  -l {critical,error,warning,info,debug}, --loglevel {critical,error,warning,info,debug}
                        the minimum level to log (default: warning)

formatters:
  -T, --test            output format: test specific (default: None)
  -D, --default         output format: human readable hierarchical text
                        (default: True)
  -G, --graphviz        output format: a Graphviz graph (default: None)
```

### Examples

#### Show references of table
`dbgraph dbnav.sqlite/article`

```
article
→ user_id → user.id
```

#### Show References and Columns
`dbgraph -c dbnav.sqlite/article`

```
article
- id*
→ user_id → user.id
- created
- title
- text
- tags?
```

#### Show all References recursively
`dbgraph -r dbnav.sqlite/article`

```
article
→ user_id → user.id
  ↑ article (user_id → user.id)
  ↑ user_address (user_id → user.id)
    → user_id → user.id
    → address_id → address.id
      ↑ user_address (address_id → address.id)
  ↑ blog_user (user_id → user.id)
    → blog_id → blog.id
      ↑ blog_user (blog_id → blog.id)
    → user_id → user.id
```

#### Show specific References
`dbgraph -i user_id.blog_user dbnav.sqlite/article`

```
article
→ user_id → user.id
  ↑ article (user_id → user.id)
  ↑ user_address (user_id → user.id)
  ↑ blog_user (user_id → user.id)
    → blog_id → blog.id
    → user_id → user.id
```

#### Show specific References and exclude others
`dbgraph -i user_id.blog_user -x user_id.blog_user.user_id dbnav.sqlite/article`

```
article
→ user_id → user.id
  ↑ article (user_id → user.id)
  ↑ user_address (user_id → user.id)
  ↑ blog_user (user_id → user.id)
    → blog_id → blog.id
```

#### Show specific References as Graphviz Graph
`dbgraph -G -i user_id dbnav.sqlite/article`

```
digraph dbgraph {
  root=article;
  article [shape="record" label="article| <id> id| <user_id> user_id| <created> created| <title> title| <text> text| <tags> tags"];
  article:user_id -> user:id [];
  user [shape="record" label="user| <id> id| <first_name> first_name| <last_name> last_name| <company> company| <username> username| <email> email| <phone> phone| <gender> gender| <url> url"];
  user_address:user_id -> user:id [];
  blog_user:user_id -> user:id [];
}
```

## Database Exporter
Exports specific rows from the database along with their references rows from other tables.

### Features
* Exports the rows matching the given URI as SQL insert statements
* Allows inclusion of referenced tables (forward and back references)
* Allows exclusion of specific columns (useful if columns are optional, or cyclic references exist)
* Takes into account the ordering of the statements (when table A references table B, then the referenced row from B must be inserted first)
* Limits the number of returned rows of the main query (does not limit referenced rows)

### Usage
```
usage: dbexport [-h] [--version] [-f LOGFILE]
                [-l {critical,error,warning,info,debug}] [-T] [-I] [-U] [-D]
                [-Y] [-i INCLUDE] [-x EXCLUDE] [-m LIMIT] [-p PACKAGE]
                uri

positional arguments:
  uri                   the URI to parse (format for PostgreSQL:
                        user@host/database/table?column=value; for SQLite:
                        databasefile.db/table?column=value)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -i INCLUDE, --include INCLUDE
                        include the specified columns and their foreign rows,
                        if any (multiple columns can be specified by
                        separating them with a comma)
  -x EXCLUDE, --exclude EXCLUDE
                        Exclude the specified columns
  -m LIMIT, --limit LIMIT
                        limit the results of the main query to this amount of
                        rows
  -p PACKAGE, --package PACKAGE
                        the package for YAML entities

logging:
  -f LOGFILE, --logfile LOGFILE
                        the file to log to
  -l {critical,error,warning,info,debug}, --loglevel {critical,error,warning,info,debug}
                        the minimum level to log

formatters:
  -T, --test            output format: test specific
  -I, --insert          output format: SQL insert statements
  -U, --update          output format: SQL update statements
  -D, --delete          output format: SQL delete statements
  -Y, --yaml            output format: YAML data
```

## Database Executer
Executes the SQL statements from the given file on the database specified by the given URI.

### Usage
```
usage: dbexec [-h] [--version] [-f LOGFILE]
              [-l {critical,error,warning,info,debug}] [-T] [-D] [-I]
              [-s STATEMENTS] [-p PROGRESS] [-n TABLE_NAME]
              uri [infile]

Executes the SQL statements from the given file on the database specified by
the given URI

positional arguments:
  uri                   the URI to parse (format for PostgreSQL:
                        user@host/database; for SQLite: databasefile.db)
  infile                the path to the file containing the SQL query to
                        execute (default: -)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -s STATEMENTS, --statements STATEMENTS
                        the statements to execute (infile will be ignored when
                        this parameter is given) (default: None)
  -p PROGRESS, --progress PROGRESS
                        show progress after this amount of executions when
                        inserting/updating large data sets (default: -1)
  -n TABLE_NAME, --table-name TABLE_NAME
                        the table name for generic select statements (default:
                        __TABLE__)

logging:
  -f LOGFILE, --logfile LOGFILE
                        the file to log to (default:
                        /usr/local/var/log/dbnav.log)
  -l {critical,error,warning,info,debug}, --loglevel {critical,error,warning,info,debug}
                        the minimum level to log (default: warning)

formatters:
  -T, --test            output format: test specific (default: None)
  -D, --default         output format: tuples (default: None)
  -I, --insert          output format: SQL insert statements (default: None)
```

## Database Differ
A diff tool that compares the structure of two database tables with each other.

### Usage
```
usage: dbdiff [-h] [--version] [-f LOGFILE]
              [-l {critical,error,warning,info,debug}] [-T] [-D] [-S] [-v]
              [-c]
              left right

A diff tool that compares the structure of two database tables with each
other.

positional arguments:
  left                  the left URI to parse (format for PostgreSQL:
                        user@host/database/table; for SQLite:
                        databasefile.db/table)
  right                 the right URI to parse (format for PostgreSQL:
                        user@host/database/table; for SQLite:
                        databasefile.db/table)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         specify the verbosity of the output, increase the
                        number of occurences of this option to increase
                        verbosity (default: None)
  -c, --compare-ddl     compares the DDLs for each column (default: False)

logging:
  -f LOGFILE, --logfile LOGFILE
                        the file to log to (default:
                        /usr/local/var/log/dbnav.log)
  -l {critical,error,warning,info,debug}, --loglevel {critical,error,warning,info,debug}
                        the minimum level to log (default: warning)

formatters:
  -T, --test            output format: test specific (default: None)
  -D, --default         output format: human readable hierarchical text
                        (default: True)
  -S, --side-by-side    output format: compare side-by-side in two columns
                        (default: None)
```

## Installation
Install the [latest egg-file](dist/dbnav-0.11.1-py2.7.egg?raw=true) from the dist directory.

```
pip install dbnav-0.11.1-py2.7.egg
```

### Alfred Workflow
To install the Alfred workflow open the [Database Navigator.alfredworkflow](dist/Database Navigator.alfredworkflow?raw=true) file from the dist directory.

## Connection Configuration
To be able to connect to a certain database you’ll need the credentials for that database. Such a connection may be added with PGAdmin (which puts it into the ~/.pgpass file) or added directly into the ~/.pgpass file.

### Sample ~/.pgpass
The ~/.pgpass file contains a connection description per line. The content of that file might look like this:

```
dbhost1:dbport:*:dbuser1:dbpass1
dbhost2:dbport:*:dbuser2:dbpass2
```

## Content Configuration
It's possible to configure the content of the result items for the Database Navigation. The configuration is placed as a table comment (currently PostgreSQL only). This is mostly helpful for displaying results in Alfred, but may come in handy for the command line tools as well.

### Usage
```
{
  "title": "{0}.fname || ' ' || {0}.lname",
  "subtitle": "{0}.email || ' (' || {0}.user_name || ')'",
  "search": ["{0}.email", "{0}.user_name"],
  "display": ["fname", "lname", "email", "user_name", "security_info_id", "staff", "disqualified", "time_zone_id", "address", "id"],
  "order": ["fname", "lname"]
}
```
### Title
The *title* is the main entry within the Alfred result item. The string *{0}* will be replaced with the table alias (useful when joining with other tables that also have the given attribute present). The replaced content will then be added to the projection list as is (SQL functions may be added as well as string concatenation as in the example above).

### Subtitle
The *subtitle* is the second line within the Alfred result item. The same replacements as with the title will be applied.

### Search
The *search* array contains the columns that will be looked into when no column is present in the Alfred query. The same replacements as with the title will be applied.

This should be used to speed up the query significantly. When no *search* is configured the generated query will look something like this (see example **Show Rows where any (Search) Column matches Pattern**):

```
select
		...
	from mytable
	where
		cast(col1 as text) like '%erber%'
		or cast(col2 as text) like '%erber%'
		...
		or cast(colN as text) like '%erber%'
```

When *search* is configured as `["col1", "col7"]` the generated query will look more like this:

```
select
		...
	from mytable
	where
		cast(col1 as text) like '%erber%'
		or cast(col7 as text) like '%erber%'
```

### Display
The *display* array contains the columns that will be added to the projection list of the SQL query. All items present in the projection list will be shown in the *values* view (see example **Show Values of selected Row**). It will be added as is (no replacements will take place).

### Order
The *order* array will be added to the *order by* part of the SQL query. It will be added as is (no replacements will take place).

## Development
If you want to change anything in the source you can build and install the project by using the make command. You’ll probably need to fiddle around with the ALFRED_WORKFLOW Makefile variable, though.

```
export ALFRED_WORKFLOW=~/Library/Application Support/Alfred 2/Alfred.alfredpreferences/workflows/user.workflow.FE656C03-5F95-4C20-AB50-92A1C286D7CD
make install
```

To simplify development you’d better use `make develop` once and have code changes reflected as soon as you save your file. Super easy development powered by [distutils](https://docs.python.org/2/distutils/index.html).

Using distutils you could easily create a Windows binary (`./setup.py bdist_msi`) or a Red Hat *rpm* package (`./setup.py bdist_rpm`).

