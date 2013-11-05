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
* Ability to filter rows by column_name=value
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

### Show Rows Matching Given Pattern
`select myuser@myhost/mydatabase/mytable/first_name=Herbert`

## Installation
```
sudo easy_install SQLAlchemy
sudo easy_install psycopg2
```
Then open the *.alfredworkflow* file created by the build.