# Alfred Database Navigator

Allows you to explore your database using Alfred 2.0.

![Alfred Database Navigator Sample](https://github.com/resamsel/alfred-dbnavigator/raw/master/docs/images/select.png "Alfred Database Navigator Sample")

## Features
* Use database connections from the `~/.pgpass` file
* Shows databases of said connections
* Shows tables of databases
* Shows rows of tables with filtering
* Shows detailed row information
* Shows info of foreign table row (based on the foreign key)
* Switch to the foreign table row
* Configuration of what is shown based on table comments
* Ability to filter rows
* Shows foreign keys that point to the current table row

## Examples
Open Alfred and type:

### Show Available Connections
`select`

### Show Databases of Connection
`select myuser@myhost/`

### Show Tables of Database
`select myuser@myhost/mydatabase/`

### Show Columns of Table
`select myuser@myhost/mydatabase/mytable/`

### Show Rows where Column equals Value
`select myuser@myhost/mydatabase/mytable/first_name=Herbert`

### Show Rows where Column matches Pattern
`select myuser@myhost/mydatabase/mytable/first_name~%erber%`

### Show Rows where any (Search) Column matches Pattern
`select myuser@myhost/mydatabase/mytable/~%erber%`

**Warning: this is a potentially slow query! See configuration for options to resolve this problem.**

### Show Values of selected Row
`select myuser@myhost/mydatabase/mytable/id=23/`

## Installation
```
sudo easy_install SQLAlchemy
sudo easy_install psycopg2
```
Then open the *.alfredworkflow* file created by the build.

## Configuration
It's possible to configure the content of the Alfred result items. This happens as a table comment (currently Postgres only).

```
{  "title": "{0}.fname || ' ' || {0}.lname",  "subtitle": "{0}.email || ' (' || {0}.user_name || ')'",  "search": ["{0}.email", "{0}.user_name"],  "display": ["fname", "lname", "email", "user_name", "security_info_id", "staff", "disqualified", "time_zone_id", "address", "id"],  "order": ["fname", "lname"]}
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
