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
Open the Alfred query window. The keyword is *select*.

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
### Features
* Visualises the dependencies of a tables using foreign keys (forward and back references)
* Optionally display columns as well as references
* Highlights primary keys (*) and optional columns (?)
* Optionally include or exclude columns/dependencies from the graph
* Optionally enable recursive inclusion (outputs each table only once, so cycles are not an issue)
* Ouput formats include hierarchical text and a Graphviz directed graph
* Uses the same configuration and URI patterns as the Database Navigator

### Usage
The command for the Database Visualisation is `dbgraph`.

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
