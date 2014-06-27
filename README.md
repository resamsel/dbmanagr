# Alfred Database Navigator

Allows you to explore your database using Alfred 2.0.

![Alfred Database Navigator Sample](https://github.com/resamsel/alfred-dbnavigator/raw/master/docs/images/select.png "Alfred Database Navigator Sample")

## Features
* Supported databases: PostgreSQL, SQLite
* Use database connection definitions from
  * the `~/.pgpass` configuration file (PGAdmin)
  * the `~/.dbexplorer/dbexplorer.cfg` configuration file (DBExplorer)
  * the Navicat configuration file (SQLite)
* Shows databases of said connections
* Shows tables of databases
* Shows columns of tables for filtering
* Shows rows of tables with filtering (operators: =, ~)
* Shows detailed row information
* Shows info of foreign table row (based on the foreign key)
* Switch to the foreign table row
* Shows foreign keys that point to the current table row
* Configuration of what is shown based on table comments

## Usage
Open the Alfred query window. The keyword is *select*.

### Show Available Connections
`dbnav`

### Show Databases of Connection
`dbnav myuser@myhost/`

### Show Tables of Database
`dbnav myuser@myhost/mydatabase/`

### Show Columns of Table
`dbnav myuser@myhost/mydatabase/mytable/`

### Show Rows where Column equals Value
`dbnav myuser@myhost/mydatabase/mytable/first_name=Herbert`

### Show Rows where Column matches Pattern
`dbnav myuser@myhost/mydatabase/mytable/first_name~%erber%`

The tilde (~) will be translated to the *like* operator in SQL. Use the percent wildcard (%) to match arbitrary strings.

### Show Rows where any (Search) Column matches Pattern
`dbnav myuser@myhost/mydatabase/mytable/~%erber%`

**Warning: this is a potentially slow query! See configuration for options to resolve this problem.**

### Show Values of selected Row
`dbnav myuser@myhost/mydatabase/mytable/id=23/`

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
