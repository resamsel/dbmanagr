alfred-dbexplorer
=================

# Alfred Database Explorer

Allows you to explore your PostgreSQL database using Alfred 2.0.

## Features
* Use database connections from the ~/.pgpass file
* Shows databases of said connections
* Shows tables of databases
* Shows rows of tables with filtering
* Shows detailed row information
* Shows info of foreign table row (based on the foreign key)
* Switch to the foreign table row
* Configuration of what is shown based on table comments
* Ability to filter rows by column_name=value

## Example
Open Alfred and type:
**select myuser@myhost/mydatabase/mytable/first_name=Herbert**