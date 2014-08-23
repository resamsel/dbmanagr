# Database Navigator

Allows you to explore, visualise and export your database. Additionally allows to explore the database using the Powerpack of Alfred 2.0.

![Alfred Database Navigator Sample](https://github.com/resamsel/alfred-dbnavigator/raw/master/docs/images/select.png "Alfred Database Navigator Sample")

## Main Features
* Database Navigation
* Database Visualisation
* Database Export
* Supported databases: PostgreSQL, SQLite
* Use database connection definitions from
  * the `~/.pgpass` configuration file (PGAdmin)
  * the `~/.dbexplorer/dbexplorer.cfg` configuration file (DBExplorer)
  * the Navicat configuration file (SQLite)
## Database Navigator
### Features
* Shows databases of configured connections
* Shows tables of databases
* Shows columns of tables for restricting rows
* Shows rows of tables with multiple restrictions (operators: =, !=, >, <, >=, <=, like)
* Shows detailed row information
* Shows info of foreign table row (based on the foreign key)
* Switch to the foreign table row (forward references)
* Shows foreign keys that point to the current table row (back references)
* Configuration of what is shown based on table comments (currently PostgreSQL only)

### Usage
Open the Alfred query window. The keyword is *dbnav*.

```
usage: dbnav [-h] [-d | -s | -j | -x | -a] [-m LIMIT] [-f LOGFILE]
             [-l LOGLEVEL]
             [uri]

positional arguments:
  uri                   The URI to parse. Format for PostgreSQL:
                        user@host/database/table/filter/; for SQLite:
                        databasefile.db/table/filter/

optional arguments:
  -h, --help            show this help message and exit
  -d, --default         use default writer
  -s, --simple          use simple writer
  -j, --json            use JSON writer
  -x, --xml             use XML writer
  -a, --autocomplete    use autocomplete writer
  -m LIMIT, --limit LIMIT
                        Limit the results of the main query to this amount of
                        rows
  -f LOGFILE, --logfile LOGFILE
                        the file to log to
  -l LOGLEVEL, --loglevel LOGLEVEL
                        the minimum level to log
```

### Examples

#### Show Available Connections
`dbnav`

#### Show Databases of Connection
`dbnav myuser@myhost/`

#### Show Tables of Database
`dbnav myuser@myhost/mydatabase/`

#### Show Columns of Table
`dbnav myuser@myhost/mydatabase/mytable/`

#### Show Rows where Column equals Value
`dbnav myuser@myhost/mydatabase/mytable/first_name=Herbert`

#### Show Rows where Column matches Pattern
`dbnav myuser@myhost/mydatabase/mytable/first_name~%erber%`

The tilde (~) will be translated to the *like* operator in SQL. Use the percent wildcard (%) to match arbitrary strings.

#### Show Rows where any (Search) Column matches Pattern
`dbnav myuser@myhost/mydatabase/mytable/~%erber%`

**Warning: this is a potentially slow query! See configuration for options to resolve this problem.**

#### Show Values of selected Row
`dbnav myuser@myhost/mydatabase/mytable/id=23/`

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
usage: dbgraph [-h] [-d | -g] [-c] [-r | -i INCLUDE] [-x EXCLUDE] [-f LOGFILE]
               [-l LOGLEVEL]
               uri

positional arguments:
  uri                   The URI to parse. Format for PostgreSQL:
                        user@host/database/table; for SQLite:
                        databasefile.db/table

optional arguments:
  -h, --help            show this help message and exit
  -d, --default         Output format: human readable hierarchical text
  -g, --graphviz        Output format: a Graphviz graph
  -c, --include-columns
                        Include columns in output (does not work with graphviz
                        as output)
  -r, --recursive       Include any forward/back reference to the starting
                        table, recursing through all tables eventually
  -i INCLUDE, --include INCLUDE
                        Include the specified columns and their foreign rows,
                        if any. Multiple columns can be specified by
                        separating them with a comma (,)
  -x EXCLUDE, --exclude EXCLUDE
                        Exclude the specified columns
  -f LOGFILE, --logfile LOGFILE
                        The file to log to
  -l LOGLEVEL, --loglevel LOGLEVEL
                        The minimum level to log
```

### Examples

#### Show references of table
`dbgraph access@localhost/access/owner`

```
owner
+ permission_id -> permission.id
```

#### Show References and Columns
`dbgraph -c access@localhost/access/owner`

```
owner
- id*
- version
- created
+ permission_id -> permission.id
- gender?
- first_name?
- last_name?
- email?
- street?
- zip_code?
- city?
- country_code?
```
#### Show all References recursively
`dbgraph -r access@localhost/access/owner`

```
owner
+ permission_id -> permission.id
  + api_key_id -> api_key.id
    + access_transaction (api_key_id -> id)
    + sales_channel (api_key_id -> id)
  + sales_channel_id -> sales_channel.id
    + teaser_template_id? -> email_template.id
  + access_transaction (permission_id -> id)
    + device_id -> device.id
    + permission_consumption (access_transaction_id -> id)
```
#### Show specific References
`dbgraph -i permission_id.api_key_id access@localhost/access/owner`

```
owner
+ permission_id -> permission.id
  + api_key_id -> api_key.id
    + access_transaction (api_key_id -> id)
    + sales_channel (api_key_id -> id)
  + sales_channel_id -> sales_channel.id
  + access_transaction (permission_id -> id)
```

#### Show specific References and exclude others
`dbgraph -i permission_id.api_key_id -x permission_id.sales_channel_id access@localhost/access/owner`

```
owner
+ permission_id -> permission.id
  + api_key_id -> api_key.id
    + access_transaction (api_key_id -> id)
    + sales_channel (api_key_id -> id)
  + access_transaction (permission_id -> id)
```

#### Show specific References as Graphviz Graph
`dbgraph -g -i permission_id access@localhost/access/owner`

```
digraph dbgraph {
  root=owner;
  owner -> permission [xlabel="permission_id -> id"];
  permission -> api_key [xlabel="api_key_id -> id"];
  permission -> sales_channel [xlabel="sales_channel_id -> id"];
  access_transaction -> permission [xlabel="permission_id -> id"];
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
usage: dbexport [-h] [-i INCLUDE] [-x EXCLUDE] [-m LIMIT] [-f LOGFILE]
                [-l LOGLEVEL]
                uri

positional arguments:
  uri                   The URI to parse. Format for PostgreSQL:
                        user@host/database/table/column=value; for SQLite:
                        databasefile.db/table/column=value

optional arguments:
  -h, --help            show this help message and exit
  -i INCLUDE, --include INCLUDE
                        Include the specified columns and their foreign rows,
                        if any. Multiple columns can be specified by
                        separating them with a comma (,)
  -x EXCLUDE, --exclude EXCLUDE
                        Exclude the specified columns
  -m LIMIT, --limit LIMIT
                        Limit the results of the main query to this amount of
                        rows
  -f LOGFILE, --logfile LOGFILE
                        the file to log to
  -l LOGLEVEL, --loglevel LOGLEVEL
                        the minimum level to log
```

## Installation
```
make install
```
Then open the *.alfredworkflow* file in the target directory using the finder.

## Configuration
It's possible to configure the content of the Alfred result items. This happens as a table comment (currently Postgres only).

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
