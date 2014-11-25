# Database Navigator

Allows you to explore, visualise and export your database. Additionally allows to explore the database using the Powerpack of Alfred 2.0.

![Alfred Database Navigator Sample](resources/images/dbnav-example.png "Alfred Database Navigator Sample")

- [Main Features](#main-features)
- [Database Navigation](#database-navigation)
	- [Features](#features)
	- [Usage](#usage)
	- [Examples](#examples)
- [Database Visualisation](#database-visualisation)
	- [Features](#features-1)
	- [Usage](#usage-1)
	- [Examples](#examples-1)
- [Database Exporter](#database-exporter)
	- [Features](#features-2)
	- [Usage](#usage-2)
	- [Examples](#examples-2)
- [Database Executer](#database-executer)
	- [Usage](#usage-3)
- [Database Differ](#database-differ)
	- [Usage](#usage-4)
	- [Examples](#examples-3)
- [Installation](#installation)
	- [Install Dependencies](#install-dependencies)
- [Homebrew on Mac OS X](#homebrew-on-mac-os-x)
- [For Debian based systems](#for-debian-based-systems)
- [For Redhat based systems](#for-redhat-based-systems)
- [Homebrew on Mac OS X](#homebrew-on-mac-os-x-1)
- [For Debian based systems](#for-debian-based-systems-1)
- [For Redhat based systems](#for-redhat-based-systems-1)
	- [Alfred Workflow](#alfred-workflow)
- [Connection Configuration](#connection-configuration)
	- [Sample ~/.pgpass](#sample-pgpass)
- [Content Configuration](#content-configuration)
	- [Usage](#usage-5)
	- [Title](#title)
	- [Subtitle](#subtitle)
	- [Search](#search)
	- [Display](#display)
	- [Order](#order)
- [Development](#development)

## Main Features
* Database Navigation
* Database Visualisation
* Database Export
* Database Execution
* Database Diff
* Supported databases: PostgreSQL, MySQL, SQLite
* Use database connection definitions from
  * the `~/.pgpass` configuration file (PGAdmin)
  * the `~/.mypass` configuration file (like `~/.pgpass`)
  * the `~/.dbexplorer/dbexplorer.cfg` configuration file (DBExplorer)
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
```
usage: dbnav [-h] [--version] [-L LOGFILE]
             [-l {critical,error,warning,info,debug}] [-T] [-D] [-S] [-J] [-X]
             [-A] [-s] [-N] [-m LIMIT]
             [uri]

A database navigation tool that shows database structure and content

positional arguments:
  uri                   the URI to parse (format for PostgreSQL/MySQL:
                        user@host/database/table?filter; for SQLite:
                        databasefile.db/table?filter)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -s, --simplify        simplify the output
  -N, --no-simplify     don't simplify the output
  -m LIMIT, --limit LIMIT
                        limit the results of the main query to this amount of
                        rows (default: 50)

logging:
  -L LOGFILE, --logfile LOGFILE
                        the file to log to
  -l {critical,error,warning,info,debug}, --loglevel {critical,error,warning,info,debug}
                        the minimum level to log

formatters:
  -T, --test            output format: test specific
  -D, --default         output format: default
  -S, --simple          output format: simple
  -J, --json            output format: JSON
  -X, --xml             output format: XML
  -A, --autocomplete    output format: autocomplete
```

In Alfred the keyword is *dbnav*. The query after the keyword is the URI to your data. No options may be given.

### Examples

#### Show Available Connections
`dbnav`

#### Show Databases of Connection
`dbnav myuser@myhost/`

#### Show Tables of Database
`dbnav dbnav.sqlite/`

Title | Subtitle
----- | --------
_comment | Table
address | Table
article | Table
blog | Table
blog_user | Table
sqlite_sequence | Table
user | Table
user2 | Table
user_address | Table

#### Show Columns of Table
`dbnav dbnav.sqlite/user?`

Title | Subtitle
----- | --------
company | user
email | user
first_name | user
gender | user
id | user
last_name | user
phone | user
url | user
username | user

#### Show Rows where Column equals Value
`dbnav dbnav.sqlite/user?first_name=Joshua`

Title | Subtitle
----- | --------
Joshua | jburtonv (id=32)
Joshua | jalexander80 (id=289)
Joshua | jpalmer8u (id=319)
Joshua | jfernandezc8 (id=441)

#### Show Rows where multiple Columns equals Value
When using the ampersand (&) in a shell make sure to escape it (prepend it with a backslash (\) in Bash), since it has a special meaning there.

`dbnav dbnav.sqlite/user?first_name=Joshua&last_name=Alexander`

Title | Subtitle
----- | --------
Joshua | jalexander80 (id=289)

#### Show Rows where Column matches Pattern
The tilde (~) will be translated to the *like* operator in SQL. Use the percent wildcard (%) to match arbitrary strings.

`dbnav dbnav.sqlite/user?first_name~%osh%`

Title | Subtitle
----- | --------
Joshua | jburtonv (id=32)
Joshua | jalexander80 (id=289)
Joshua | jpalmer8u (id=319)
Joshua | jfernandezc8 (id=441)

#### Show Rows where Column is in List
The colon (:) will be translated to the *in* operator in SQL.

`dbnav dbnav.sqlite/user?first_name:Herbert,Josh,Martin`

Title | Subtitle
----- | --------
Martin | mrichardsonp (id=26)
Martin | mdiaze1 (id=506)

#### Show Rows where any (Search) Column matches Pattern
`dbnav myuser@myhost/mydatabase/mytable?~%erber%`

**Warning: this is a potentially slow query! See configuration for options to resolve this problem.**

#### Show Values of selected Row
`dbnav dbnav.sqlite/user/?id=2`

Title | Subtitle
----- | --------
2 | user.id
Evelyn | user.first_name
Gardner | user.last_name
 | user.company
egardner1 | user.username
 | user.email
8-(549)755-1011 | user.phone
Female | user.gender
 | user.url
← article.user_id | article.user_id
← blog_user.user_id | blog_user.user_id
← user_address.user_id | user_address.user_id

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
usage: dbgraph [-h] [--version] [-L LOGFILE]
               [-l {critical,error,warning,info,debug}] [-T] [-D] [-G] [-c]
               [-C] [--back-references] [--no-back-references] [--driver]
               [--no-driver] [--connection] [--no-connection] [--database]
               [--no-database] [-M MAX_DEPTH] [-r | -i INCLUDE] [-x EXCLUDE]
               [-v]
               uri

A database visualisation tool that creates graphs from the database structure

positional arguments:
  uri                   the URI to parse (format for PostgreSQL/MySQL:
                        user@host/database/table; for SQLite:
                        databasefile.db/table)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -c, --columns         include columns in output
  -C, --no-columns      don't include columns in output
  --back-references     include back references in output
  --no-back-references  don't include back references in output
  --driver              include database driver in output (does not work well
                        with graphviz as output)
  --no-driver           don't include database driver in output
  --connection          include connection in output (does not work well with
                        graphviz as output)
  --no-connection       don't include connection in output
  --database            include database in output (does not work well with
                        graphviz as output)
  --no-database         don't include database in output
  -M MAX_DEPTH, --max-depth MAX_DEPTH
                        the maximum depth to use in recursion/inclusion
                        (default: -1)
  -r, --recursive       include any forward/back reference to the starting
                        table, recursing through all tables eventually
  -i INCLUDE, --include INCLUDE
                        include the specified columns and their foreign rows,
                        if any. Multiple columns can be specified by
                        separating them with a comma (,)
  -x EXCLUDE, --exclude EXCLUDE
                        exclude the specified columns
  -v, --verbose         specify the verbosity of the output, increase the
                        number of occurences of this option to increase
                        verbosity

logging:
  -L LOGFILE, --logfile LOGFILE
                        the file to log to
  -l {critical,error,warning,info,debug}, --loglevel {critical,error,warning,info,debug}
                        the minimum level to log

formatters:
  -T, --test            output format: test specific
  -D, --default         output format: human readable hierarchical text
  -G, --graphviz        output format: a Graphviz graph
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
usage: dbexport [-h] [--version] [-L LOGFILE]
                [-l {critical,error,warning,info,debug}] [-T] [-I] [-U] [-D]
                [-Y] [-F] [-i INCLUDE] [-x EXCLUDE] [-m LIMIT] [-p PACKAGE]
                [-f FORMAT]
                uri

An export tool that exports database rows in different formats.

positional arguments:
  uri                   the URI to parse (format for PostgreSQL/MySQL:
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
                        rows (default: 50)
  -p PACKAGE, --package PACKAGE
                        the package for YAML entities (default: models)
  -f FORMAT, --format FORMAT
                        the format for the -F/--formatted writer (use {0} for
                        positional arguments, or {column_name} to insert the
                        actual value of table.column_name) (default: {0})

logging:
  -L LOGFILE, --logfile LOGFILE
                        the file to log to
  -l {critical,error,warning,info,debug}, --loglevel {critical,error,warning,info,debug}
                        the minimum level to log

formatters:
  -T, --test            output format: test specific
  -I, --insert          output format: SQL insert statements
  -U, --update          output format: SQL update statements
  -D, --delete          output format: SQL delete statements
  -Y, --yaml            output format: YAML data
  -F, --formatted       output format: given with the -f/--format option
```

### Examples

#### Export Contents of Table
`dbexport dbnav.sqlite/article?id=2`

```
insert into article (id,user_id,created,title,text,tags) values (2,960,'2014-03-01 21:51:18','duis bibendum morbi','urna ut tellus nulla ut erat id mauris vulputate elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in consequat ut nulla sed accumsan felis ut at','vestibulum aliquet ultrices erat tortor sollicitudin');
```

#### Export limited Contents of Table
`dbexport -m 1 dbnav.sqlite/article?*`

```
insert into article (id,user_id,created,title,text,tags) values (1,558,'2013-10-29 06:54:06','quam pharetra magna ac','montes nascetur ridiculus mus vivamus vestibulum sagittis sapien cum sociis natoque penatibus et magnis dis parturient montes nascetur ridiculus mus etiam vel augue vestibulum rutrum rutrum neque aenean auctor gravida sem praesent id massa id nisl venenatis lacinia aenean sit amet justo morbi ut odio cras mi pede malesuada in imperdiet et commodo vulputate justo in blandit ultrices enim lorem ipsum dolor sit amet consectetuer adipiscing elit proin interdum mauris non ligula pellentesque ultrices phasellus id sapien in sapien iaculis congue vivamus','');
```

#### Export Contents of Table with Specific References
`dbexport -i user_id dbnav.sqlite/article?id=2`

```
insert into "user" (id,first_name,last_name,company,username,email,phone,gender,url) values (960,'Todd','Willis','','twillisqn','twillisqn@ovh.net','','Male','http://epa.gov/in/hac.html?nisi=lobortis&at=convallis&nibh=tortor&in=risus&hac=dapibus&habitasse=augue&platea=vel&dictumst=accumsan&aliquam=tellus&augue=nisi&quam=eu&sollicitudin=orci&vitae=mauris&consectetuer=lacinia&eget=sapien&rutrum=quis&at=libero&lorem=nullam&integer=sit&tincidunt=amet&ante=turpis&vel=elementum&ipsum=ligula&praesent=vehicula&blandit=consequat&lacinia=morbi&erat=a&vestibulum=ipsum&sed=integer&magna=a&at=nibh&nunc=in&commodo=quis&placerat=justo&praesent=maecenas&blandit=rhoncus&nam=aliquam&nulla=lacus&integer=morbi&pede=quis&justo=tortor&lacinia=id&eget=nulla&tincidunt=ultrices&eget=aliquet&tempus=maecenas&vel=leo&pede=odio&morbi=condimentum&porttitor=id&lorem=luctus&id=nec&ligula=molestie&suspendisse=sed&ornare=justo&consequat=pellentesque&lectus=viverra&in=pede&est=ac&risus=diam&auctor=cras&sed=pellentesque&tristique=volutpat&in=dui&tempus=maecenas&sit=tristique&amet=est&sem=et&fusce=tempus&consequat=semper');
insert into article (id,user_id,created,title,text,tags) values (2,960,'2014-03-01 21:51:18','duis bibendum morbi','urna ut tellus nulla ut erat id mauris vulputate elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in consequat ut nulla sed accumsan felis ut at','vestibulum aliquet ultrices erat tortor sollicitudin');
```

#### Export Contents of Table with Specific References and exclude columns
`dbexport -i user_id -x user_id.url,text dbnav.sqlite/article?id=2`

```
insert into "user" (id,first_name,last_name,company,username,email,phone,gender) values (960,'Todd','Willis','','twillisqn','twillisqn@ovh.net','','Male');
insert into article (id,user_id,created,title,tags) values (2,960,'2014-03-01 21:51:18','duis bibendum morbi','vestibulum aliquet ultrices erat tortor sollicitudin');
```

#### Export Contents of Table as Update Statements
`dbexport -U dbnav.sqlite/article?id=2`

```
update article set user_id = 960, created = '2014-03-01 21:51:18', title = 'duis bibendum morbi', text = 'urna ut tellus nulla ut erat id mauris vulputate elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in consequat ut nulla sed accumsan felis ut at', tags = 'vestibulum aliquet ultrices erat tortor sollicitudin' where id = 2;
```

#### Export Contents of Table as Delete Statements
`dbexport -D dbnav.sqlite/article?id=2`

```
delete from article where id = 2;
```

#### Export Contents of Table as YAML
`dbexport -Y dbnav.sqlite/article?id=2 -p my.models`

```
articles:
    - &article_2 !!my.models.Article
        id: !!int 2
        user: *user_!!int 960
        created: 2014-03-01 21:51:18
        title: duis bibendum morbi
        text: urna ut tellus nulla ut erat id mauris vulputate elementum nullam varius nulla facilisi cras non velit nec nisi vulputate nonummy maecenas tincidunt lacus at velit vivamus vel nulla eget eros elementum pellentesque quisque porta volutpat erat quisque erat eros viverra eget congue eget semper rutrum nulla nunc purus phasellus in felis donec semper sapien a libero nam dui proin leo odio porttitor id consequat in consequat ut nulla sed accumsan felis ut at
        tags: vestibulum aliquet ultrices erat tortor sollicitudin
```

## Database Executer
Executes the SQL statements from the given file on the database specified by the given URI.

### Usage
```
usage: dbexec [-h] [--version] [-L LOGFILE]
              [-l {critical,error,warning,info,debug}] [-T] [-D] [-I]
              [-s STATEMENTS] [-p PROGRESS] [-n TABLE_NAME]
              uri [infile]

Executes the SQL statements from the given file on the database specified by
the given URI

positional arguments:
  uri                   the URI to parse (format for PostgreSQL/MySQL:
                        user@host/database; for SQLite: databasefile.db)
  infile                the path to the file containing the SQL query to
                        execute

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -s STATEMENTS, --statements STATEMENTS
                        the statements to execute (infile will be ignored when
                        this parameter is given)
  -p PROGRESS, --progress PROGRESS
                        show progress after this amount of executions when
                        inserting/updating large data sets (default: -1)
  -n TABLE_NAME, --table-name TABLE_NAME
                        the table name for generic select statements (default:
                        __TABLE__)

logging:
  -L LOGFILE, --logfile LOGFILE
                        the file to log to
  -l {critical,error,warning,info,debug}, --loglevel {critical,error,warning,info,debug}
                        the minimum level to log

formatters:
  -T, --test            output format: test specific
  -D, --default         output format: tuples
  -I, --insert          output format: SQL insert statements
```

## Database Differ
A diff tool that compares the structure of two database tables with each other.

### Usage
```
usage: dbdiff [-h] [--version] [-L LOGFILE]
              [-l {critical,error,warning,info,debug}] [-T] [-D] [-S] [-v]
              [-c]
              left right

A diff tool that compares the structure of two database tables with each
other.

positional arguments:
  left                  the left URI to parse (format for PostgreSQL/MySQL:
                        user@host/database/table; for SQLite:
                        databasefile.db/table)
  right                 the right URI to parse (format for PostgreSQL/MySQL:
                        user@host/database/table; for SQLite:
                        databasefile.db/table)

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -v, --verbose         specify the verbosity of the output, increase the
                        number of occurences of this option to increase
                        verbosity
  -c, --compare-ddl     compares the DDLs for each column

logging:
  -L LOGFILE, --logfile LOGFILE
                        the file to log to
  -l {critical,error,warning,info,debug}, --loglevel {critical,error,warning,info,debug}
                        the minimum level to log

formatters:
  -T, --test            output format: test specific
  -D, --default         output format: human readable hierarchical text
  -S, --side-by-side    output format: compare side-by-side in two columns
```

### Examples

#### Diff two Tables
`dbdiff dbnav.sqlite/user dbnav.sqlite/user2`

```
< url
< company
> company_name
> title
```

#### Diff two Tables Side-by-Side
`dbdiff -S dbnav.sqlite/user dbnav.sqlite/user2`

```
url                                        <
company                                    <
                                           > company_name
                                           > title
```

#### Diff two Tables Side-by-Side using Column Definitions
`dbdiff -Sc dbnav.sqlite/user dbnav.sqlite/user2`

```
username TEXT(31)                          | username TEXT(31) not null
first_name TEXT(255) not null              | first_name TEXT(127) not null
                                           > title TEXT(127)
url TEXT(255)                              <
company TEXT(255)                          <
                                           > company_name TEXT(255)
```

## Installation
Install the [latest egg-file](dist/dbnav-0.16-py2.7.egg?raw=true) from the dist directory.

```
easy_install dbnav-0.16-py2.7.egg
```

### Install Dependencies

You need PostgreSQL and MySQL installed to access those databases. [Homebrew](http://brew.sh/) can help you with that:

#### PostgreSQL

```
## Homebrew on Mac OS X
brew install postgresql9
## For Debian based systems
#apt-get install postgresql
## For Redhat based systems
#yum install postgresql
pip install psycopg2
```

#### MySQL

```
## Homebrew on Mac OS X
brew install mysql
## For Debian based systems
#apt-get install mysql
## For Redhat based systems
#yum install mysql
pip install mysql-python
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
  "title": "{first_name} {last_name}",
  "subtitle": "{email} ({username})",
  "search": ["email", "username"],
  "display": ["first_name", "last_name", "email", "username", "id"],
  "order": ["first_name", "last_name"]
}
```
### Title
The *title* is the main entry within the Alfred result item. The content will be used as the format within the string.format() method.

### Subtitle
The *subtitle* is the second line within the Alfred result item. See [Title](#title) for details.

### Search
The *search* array contains the columns that will be looked into when no filter column is present in the query string.

This should be used to speed up the query significantly. When no *search* is configured the generated query will look something like this (see example **Show Rows where any (Search) Column matches Pattern**), where *n* is the amount of columns of the table (*n = |table.columns|*):

```
select
		...
	from mytable
	where
		cast(col1 as text) like '%erber%'
		or cast(col2 as text) like '%erber%'
		...
		or cast(coln as text) like '%erber%'
```

When *search* is configured as `["col1", "col7"]` the generated query will look more like this (two filter expressions instead of *n*):

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

