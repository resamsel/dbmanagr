Changelog
=========

v0.28.3 (2015-10-11)
--------------------

Changes
~~~~~~~

- Adapt signing. [René Samselnig]

v0.28.2 (2015-10-11)
--------------------

Changes
~~~~~~~

- Removes alfred workflow temporarily. [René Samselnig]

- Updates badges for PyPI. [René Samselnig]

- Migrates package name to dbmanagr. [René Samselnig]

Fix
~~~

- Fixes links in documentation. [René Samselnig]

- Fixes Travis CI build. [René Samselnig]

v0.28.1 (2015-10-08)
--------------------

Fix
~~~

- Fixes failing test. [René Samselnig]

v0.28.0 (2015-10-08)
--------------------

Changes
~~~~~~~

- Renaming to Database Managr (dbmanagr). [René Samselnig]

- Simplifies Makefile. [René Samselnig]

- Adds example images in documentation. [René Samselnig]

Fix
~~~

- Fixes formatting of unicode strings. #17. [René Samselnig]

v0.27.0 (2015-09-03)
--------------------

New
~~~

- Adds a pattern to filter results in dbstat. #16. [René Samselnig]

- Removes a few columns from the default view of dbstat. #15. [René
  Samselnig]

- More tests. [René Samselnig]

- Adds tests for special code cases. [René Samselnig]

- Adds tests for several missing lines of code. [René Samselnig]

Changes
~~~~~~~

- Disables code coverage check on remote execution (daemon), because it
  cannot be tested reliably. The daemon forks a new process, which also
  affects the currently running tests. They get executed two times, in
  parallel, as soon as the daemon forks. Currently, I see no possibility
  to avoid this behaviour (other than to mock the daemon in tests).
  [René Samselnig]

- Renames dbstat to dbstac. [René Samselnig]

Fix
~~~

- Removes unused code. [René Samselnig]

- Fixes default value of dbexec command to allow reading from stdin.
  [René Samselnig]

- Reverting back to sqlalchemy 0.9.10. [René Samselnig]

- Using newest sqlalchemy version that doesn't fix the bug regarding
  __dict__. #13. [René Samselnig]

v0.26.3 (2015-08-31)
--------------------

New
~~~

- Tests added. [René Samselnig]

- Tests added that increase the code coverage. [René Samselnig]

v0.26.2 (2015-08-25)
--------------------

New
~~~

- Adds coveralls coverage status. [René Samselnig]

- Adds coveralls.io to measure code metrics. [René Samselnig]

v0.26.1 (2015-08-25)
--------------------

New
~~~

- Tests for the argumentor. [René Samselnig]

Changes
~~~~~~~

- Migrates grapher to use the content selection dict instead of a string
  array. [René Samselnig]

- Improves the output of the grapher YAML format. [René Samselnig]

Fix
~~~

- Tries to fix Travis build. [René Samselnig]

- Fixes tests. [René Samselnig]

v0.26.0 (2015-08-19)
--------------------

New
~~~

- Adds a YAML writer for the grapher, which can then be used to create a
  template config file usable for dbargs. [René Samselnig]

- Adds new tool to create command line arguments from a YAML config
  file. [René Samselnig]

- Adds a .travis.yml config file for Travis CI. [René Samselnig]

Fix
~~~

- Workaround for #13. [René Samselnig]

- Unicode char in string. [René Samselnig]

- Adds another test dependency. [René Samselnig]

- Adds test dependencies. [René Samselnig]

- Removes the installation of the bash completiton. [René Samselnig]

- Fixes the Travis build. [René Samselnig]

Other
~~~~~

- Fixes using wrong column in exports. [René Samselnig]

- Works around a bug (?) in an older python version. [René Samselnig]

- Works around a bug (?) in an older python version. [René Samselnig]

- Fixes replacing dependency in setup.py. [René Samselnig]

- Replaces mysql-python with pymysql (pure python). [René Samselnig]

- Also, reflect this change in the generated README.md. [René
  Samselnig]

- Changes order of the info images in the documentation. [René
  Samselnig]

- Another try to enable tests. [René Samselnig]

- Updates README.md with build status information. [René Samselnig]

- Updates README.md with build status information. [René Samselnig]

- Updates README.md with build status information. [René Samselnig]

- Temporarily exclude tests. [René Samselnig]

- Create the target directories in travis. [René Samselnig]

- Migrates tests to mysql-python mysql module. [René Samselnig]

- Migrates tests to pg8000 postgres module. [René Samselnig]

- Hopefully fixes last landscape.io code smells. [René Samselnig]

v0.25.0 (2015-04-07)
--------------------

- Fixes some landscape.io code smells. [René Samselnig]

- Fixes some landscape.io code smells. [René Samselnig]

- Fixes some landscape.io code smells. [René Samselnig]

- Removes the cyclic imports. [René Samselnig]

- Fixes some landscape.io code smells. [René Samselnig]

- Fixes some landscape.io code smells. [René Samselnig]

- Fixes some landscape.io code smells. [René Samselnig]

- Fixes some landscape.io code smells. [René Samselnig]

v0.24.0 (2015-04-01)
--------------------

- Implements #12 for commands differ, executer, grapher and navigator.
  [René Samselnig]

- Removes some circular dependency. [René Samselnig]

- Another try on the cyclic dependencies issue. [René Samselnig]

- Probably fixes cyclic dependencies this time? [René Samselnig]

- Probably fixes cyclic import. [René Samselnig]

- Adds code metric tool pylint to be run before testing the actual code.
  [René Samselnig]

- Probably fixes the landscape issue. [René Samselnig]

- Removes complexity D from the project (radon cc). [René Samselnig]

- Fixes tests involving the output of commands. [René Samselnig]

- Revert "Removes landscape.io config options." [René Samselnig]

  This reverts commit b62c71fac06c3d58af4c63f64d922fb7f84f48ce.

- Removes landscape.io config options. [René Samselnig]

- Fixes most errors mentioned by landscape.io. [René Samselnig]

- Adds the ability to substitute values of rows with given, static ones.
  This is available in the Insert and Yaml formatters of the exporter.
  [René Samselnig]

- Removes the egg file from the dist directory. [René Samselnig]

v0.23.0 (2015-02-26)
--------------------

- Enhances dbstat command. Fixes #11. [René Samselnig]

- Adds options to the status command. [René Samselnig]

- Adds the dbstat command that shows statement activity (ATM PostgreSQL
  only). [René Samselnig]

- Fixes missing loglevel configuration. [René Samselnig]

- Adds stub for dbstat. [René Samselnig]

- Improves coverage. [René Samselnig]

- Fixes YAML writer. [René Samselnig]

v0.22.0 (2015-01-22)
--------------------

- Temporary re-add. [René Samselnig]

- Finishes integration of navigator into daemon. Navigator uses separate
  DTOs (saves bandwidth). [René Samselnig]

- Fixes tests for the daemon. [René Samselnig]

- Fixes alfred workflow. [René Samselnig]

- Migrates navigator to DTOs. [René Samselnig]

- Adds separate tests for the daemon. [René Samselnig]

- Removes the XML writer/formatter. [René Samselnig]

- Updates grapher and differ to work with the daemon. Executer seems to
  work with the daemon as well. [René Samselnig]

- Refactors node.py into grapher module. [René Samselnig]

- Fixes failing tests. Exporter works now with DTOs. [René Samselnig]

- Adds foreign keys to the table DTO. [René Samselnig]

- First step towards DTOs. [René Samselnig]

- Fixes flake8 errors. [René Samselnig]

- Includes the daemon process into the infrastructure. Adds a dbdaemon
  command to allow starting, stopping and statusing the daemon. Exporter
  has been ported already. [René Samselnig]

- Adds daemon process that executes commands given as HTTP POST
  requests. Adds client that uses json file and sends it to writer.
  [René Samselnig]

v0.21.0 (2015-01-13)
--------------------

- Implements #8: Allow wildcard in exclude in dbexport. Also allows
  wildcards in include. [René Samselnig]

v0.20.0 (2015-01-02)
--------------------

- Reverts removing subtitle and icon of Column. Adds tests for those
  cases. [René Samselnig]

- Adds a verbose option to dbexec to allow writing out the current
  query. [René Samselnig]

- Changes sqlalchemy binary operators to method calls. [René Samselnig]

- Fixes missing code coverage (make clean now does a proper clean and
  removes .coverage files as well). Adds tests to achieve full code
  coverage. Adds step towards branch coverage (instrumental). [René
  Samselnig]

- Removes paths only available on my system. [René Samselnig]

- Adds the AnyFilePassSource to allow for a ~/.sqlitepass config file.
  Cleans up test config files. [René Samselnig]

v0.19.0 (2014-12-29)
--------------------

- Simplifies driver code. [René Samselnig]

- Moves drivers to dbnav.driver package. Simplifies drivers (extracts
  sources). [René Samselnig]

- Migrates logduration to LogTimer. [René Samselnig]

- Migrates sources.py into separate module (additional sources should be
  placed in there). [René Samselnig]

- Some more refactoring. [René Samselnig]

- Moves options to driver. [René Samselnig]

v0.18.1 (2014-12-18)
--------------------

- Fixes doc. [René Samselnig]

- Adds option --isolate-statements, which isolates each statement in a
  separate transaction (previously --ignore-errors). Adds option --mute-
  errors, which prevents error messages from SQL statements from being
  written to stdout. [René Samselnig]

- Migrates documentation to the wiki. [René Samselnig]

v0.18.0 (2014-12-17)
--------------------

- - Migrates MySQL options to driver - Adds dbexec --ignore-errors
  option - Print results as soon as they are available in dbexec. [René
  Samselnig]

- Adds more tests (coverage: 100%). Fixes issue with dbnav -N. [René
  Samselnig]

- Adds more tests (coverage: 99%). [René Samselnig]

- Adds more tests (coverage: 98%). [René Samselnig]

- Adds more tests (coverage: 97%). [René Samselnig]

- Adds more test cases. [René Samselnig]

- Adds tests to boost coverage to 90%. [René Samselnig]

- Migrates to nosetests with coverage. [René Samselnig]

- Adds licence information to all python files. [René Samselnig]

- Enhances logging. [René Samselnig]

- Migrates the @decorator to a Wrapper class. Makes it more flexible to
  use as a library. Also, migrates some code only used in the navigator
  to the navigator. [René Samselnig]

- Fixes and tests unicode encoding issue. [René Samselnig]

- Makes alfred workflow updatable in principle. [René Samselnig]

- Fixes documentation. [René Samselnig]

- Fixes wiki links. [René Samselnig]

- Fixes wiki links. [René Samselnig]

- Migrates documentation to the wiki. [René Samselnig]

- Fixes TOC. [René Samselnig]

- Fixes path of example image in doc. [René Samselnig]

v0.17.0 (2014-12-01)
--------------------

- Adds the OR operator (|). Adds tests for sources. [René Samselnig]

- Adds the alfred-workflow library to display items within Alfred.
  [René Samselnig]

- Implements #5 (dry run). [René Samselnig]

- Fixes #4. [René Samselnig]

- Adds tests for exception, logger, model.databaseconnection. [René
  Samselnig]

- Adds tests for options.restriction and .format_value. [René
  Samselnig]

- Adds tests for escape_keyword. [René Samselnig]

- Adds pg8000 plugin. [René Samselnig]

- Adds sqlalchemy plugin py-postgresql, if psycopg2 not available. Lists
  found drivers with --version. [René Samselnig]

- Adds tuning options for database drivers (connection string may be
  enhanced with options). [René Samselnig]

- Adds multiple implementation options for MySQL. [René Samselnig]

- Enables installation without PostgreSQL or MySQL installed. Support
  for those databases will be enabled as soon as either psycopg2 or
  mysql-python gets installed (see section Installation in README.md).
  [René Samselnig]

- Refactors connection out of class Table. Replaces mock data with real
  data from test database. Fixes #6. [René Samselnig]

- Adds test cases for utils.py, comment.py, querybuilder.py. [René
  Samselnig]

- Adds tests for utils.py. [René Samselnig]

- Updates documentation of content configuration. [René Samselnig]

- Code simplification. [René Samselnig]

- More sane defaults for title and subtitle. [René Samselnig]

- Updates documentation with additional installation info. [René
  Samselnig]

- Removes defaults from most options, but leave it where it makes sense.
  [René Samselnig]

- Fixes subtitles. [René Samselnig]

- Fixes using arbitrary number of forward references in filters.
  Replaces column extraction with inspector with MetaData. [René
  Samselnig]

- Adds the ability to join tables on the fly (i.e.
  article?user_id.first_name=Willie). [René Samselnig]

- Moves loglevel parsing to argparse action. [René Samselnig]

- Makes setup.py flake8 clean. [René Samselnig]

- Finally removes tests from distribution. [René Samselnig]

- Uses a factory method for creating the Comment. [René Samselnig]

- Adds more flake8 checks. Adds verbose option to dbgraph to display
  column definitions. [René Samselnig]

- Refactors code into method to make it ready for recursion. [René
  Samselnig]

- Fixes using @ in query. Fixes naming conventions. [René Samselnig]

- Adds option to display certain columns in simplify mode. [René
  Samselnig]

- Refactors the create_title method into utils. [René Samselnig]

- Adds testcase for searching search fields (comments). [René
  Samselnig]

- Adds test for display comment. [René Samselnig]

- Adds _comment table to retrieve comments from. [René Samselnig]

- Improves the log decorator. [René Samselnig]

- Fixes log decorator for unicode results. [René Samselnig]

- Fixes backwards compatibility. [René Samselnig]

- Restructures the project. [René Samselnig]

- Makes dbnav flake8 clean. Fixes failing tests. [René Samselnig]

- Fixes some E501 and E128 flake8 errors. [René Samselnig]

- Documentation update. [René Samselnig]

- Test hook2. [René Samselnig]

- Test hook. [René Samselnig]

- Fixes all flake8 warnings. [René Samselnig]

- Fixes all flake8 errors but E128 (which will take some more time).
  [René Samselnig]

- Fixes E302 expected 2 blank lines, found 1. [René Samselnig]

- Adds flake8 checks to tests. Fixes flake8 failures. Removes several
  errors. [René Samselnig]

- Migration to a more robust query filter. [René Samselnig]

- Removes some boilerplate code. [René Samselnig]

- Extracts the arguments to a separate module. [René Samselnig]

- Adds the -Ff formatter options to format the result accordingly.
  [René Samselnig]

- Adds the sqlalchemy ORM layer to build the query with. [René
  Samselnig]

- Adds generated TOC to README.md. [René Samselnig]

- Fixes error handling for dbnav. [René Samselnig]

- Fixes default values of method parameters. [René Samselnig]

- Fixes README.md. [René Samselnig]

- Place notes at the top of the example for better understanding the
  example. [René Samselnig]

- Removes backup table. [René Samselnig]

- Updates the differ tests and documentation with more sophisticated
  examples. [René Samselnig]

- Adds/updates tests of the exporter. [René Samselnig]

- Adds tests for the differ. [René Samselnig]

- Test resources cleanup. [René Samselnig]

- Adds documentation for MySQL. [René Samselnig]

- Fixes the documentation with tables. [René Samselnig]

- Another one. [René Samselnig]

- Next try. [René Samselnig]

- Changes example results to be displayed as tables. [René Samselnig]

- Fixes list of databases in MySQL. [René Samselnig]

- Support MySQL #1. [René Samselnig]

  Adds MySQL support.

- Adds examples for dbexport. [René Samselnig]

- Adds missing parameter. [René Samselnig]

- Bumps version to 0.11.1 (documentation fix). [René Samselnig]

- Adds a shell 'template' that generates the README.md. [René
  Samselnig]

- Bumps version to 0.11. [René Samselnig]

- Adds a perl script that generates the usage documentation in
  README.md. [René Samselnig]

- Fixes autocomplete results of tables and columns/values. Fixes typo in
  README. [René Samselnig]

- Some code cleanup, fixes bash completion. [René Samselnig]

- Moves tests to the root package. [René Samselnig]

- Fixes tests. [René Samselnig]

- Adds a SQLite database with test data. [René Samselnig]

- May now also be used as a shell interpreter: [René Samselnig]

  ```
  #!/usr/bin/env dbexec user@host/database

  select * from table;
  ```

- Adds foreign keys for SQLite connections. [René Samselnig]

- Adds the side-by-side option. [René Samselnig]

- Changes the default format of dbnav. [René Samselnig]

- Unification of the output formatter options (always use capitalised
  letters). [René Samselnig]

- Adds the ability to compare the DDL of the columns instead of only the
  name. [René Samselnig]

- Bumps version to 0.10. [René Samselnig]

- Updates the documentation. [René Samselnig]

- Adds the dbdiff tool to compare database tables. [René Samselnig]

- Fixes queries with like on integer columns (i.e. ...?id~370%,
  ...?id~370). [René Samselnig]

- Adds an UnknownColumnException with optional close matches displayed.
  [René Samselnig]

- Bumps version to 0.9.1. [René Samselnig]

- Fixes exception with unknown dictionary keys. [René Samselnig]

- Adds the option to name the table in dbexec. [René Samselnig]

- Removes duplicates from exported items. [René Samselnig]

- Adds the in operator (colon in URIs) -> user@host/db/table?id:1,2,3,4
  . [René Samselnig]

- Adds new version to README. [René Samselnig]

- Adds new version to README. [René Samselnig]

- Bump to version 0.9. [René Samselnig]

- Fixes YAML values None, bool, int, and float. Fixes field names. Adds
  option for package name. Fixes references to other entities. [René
  Samselnig]

- Adds YAML output formatter for the exporter. [René Samselnig]

- Adds documentation for a sample database connection configuration
  (~/.pgpass). [René Samselnig]

- Creates new release 0.8. [René Samselnig]

- Creates section about dbnav development. [René Samselnig]

- Adds the alfred workflow binary to the dist directory, too. [René
  Samselnig]

- Link to the raw file? [René Samselnig]

- Adds more documentation. Adds the binary distribution to the
  repository to be able to link to it. [René Samselnig]

- Clarifies command line parameters. Adds columns to graphviz output.
  [René Samselnig]

- Release v0.7. [René Samselnig]

- Simplifies argument parsing and evaluation. Fixes a problem with nan
  floats. Fixes some testcases. [René Samselnig]

- Changes the URI from user@host/database/table/filter&filter to
  user@host/database/table?filter&filter. [René Samselnig]

- Moves executer, exporter, grapher and navigator to separate modules.
  [René Samselnig]

- Unifies command line arguments. Fixes tests. [René Samselnig]

- Removes the id from the update list. [René Samselnig]

- Adds an option to output SQL update instead of insert statements.
  Documentation updates. [René Samselnig]

- Creates release v0.6. [René Samselnig]

- Adds test for the database, connection, driver options. [René
  Samselnig]

- Adds options to display connection, database and driver in dbgraph.
  [René Samselnig]

- Adds the Database Executer. [René Samselnig]

- Adds the ability to filter null values (column=null -> column is null,
  column!=null -> column is not null). Potential semantic clash with an
  actual value 'null'... [René Samselnig]

- Write a nice error message. [René Samselnig]

- Adds tests for grapher and exporter as well. [René Samselnig]

- Adds new testcase. [René Samselnig]

- Fixes working with BLOBs. [René Samselnig]

- Fixes encoding error in unicode arguments. [René Samselnig]

- Force displaying the whole error message. [René Samselnig]

- Refactors tests. [René Samselnig]

- Fixes include and exclude with breadth first search. [René Samselnig]

- Updates table of contents. [René Samselnig]

- Adds a table of contents. [René Samselnig]

- Adds the usage of dbnav, dbgraph and dbexport. [René Samselnig]

- Fixes missing re import. Updates README.md. [René Samselnig]

- Adds an error recovery format for the writer. [René Samselnig]

- Simplifies writers. [René Samselnig]

- Uses deque as data structure. [René Samselnig]

- Adds recursive graph creation (using a breadth first search
  algorithm). Adds graphviz output format. Adds an option to
  additionally display non foreign key columns. Removes deprecated debug
  messages. Adds a new operator not equals (!=). [René Samselnig]

- Refactors code. [René Samselnig]

- Adds columns to output, too. [René Samselnig]

- Better visualisation of graph. [René Samselnig]

- Adds a graph from the database. [René Samselnig]

- Allows for multiple filters (& is the separator). [René Samselnig]

- Fixes issues with some datatypes (bool, datetime). [René Samselnig]

- Fixes last failing test case. Renames dbexp to dbexport. [René
  Samselnig]

- Better checks of include/exclude columns. Better exception handling.
  [René Samselnig]

- Adds the database exporter. Use it like this: [René Samselnig]

  dbexp \
  	-x ticket_corner_id,created_by_api_key_id,communicated_to_ticket_corner,current_season_statistics,privacy_rankings_user_name,address.federal_state,race_profile.current_ski,race_profile.current_snowboard,current_fitness_profile.user_id \
  	-i address,newsfeed,current_fitness_profile,race_profile,address.country,security_info_id \
  	skiline@localhost/skiline/user/version\>10000

- Creating release 0.5. [René Samselnig]

- Fixes Alfred workflow for search queries with ampersands (&). Fixes
  casting problems. [René Samselnig]

- Release 0.4.1. [René Samselnig]

- Fixes reporting errors to the frontend (Alfred). [René Samselnig]

- Creates the 0.4 release. [René Samselnig]

- Minor output changes to better reflect foreign key values. [René
  Samselnig]

- Cleans tests. Makes title, subtitle and autocomplete texts come from
  their respective classes rather than from the code that creates the
  output. [René Samselnig]

- Fixes databases query for postgres for super users. [René Samselnig]

- Fixes autocomplete uris and corresponding tests. [René Samselnig]

- Fixes format of sqlite database URIs (added slash at the end). Adds
  fixes sorting by title of several result types. [René Samselnig]

- Fixes doc. [René Samselnig]

- Moves to 0.3. [René Samselnig]

- Fixes mysterious issue with param order=[] gets value ['_api_key.id']
  when *not* provided as method parameter. [René Samselnig]

- Migrates shell script test case invocation to python unittests. [René
  Samselnig]

- Allows missing config files. [René Samselnig]

- Updates the documentation. [René Samselnig]

- Adds make target to create and install an egg file. Adds bash
  completion support. [René Samselnig]

- Makes testing more general (no test.py needed any longer). Fixes some
  ProgrammingErrors. [René Samselnig]

- Adds more documentation. [René Samselnig]

- More documentation. [René Samselnig]

- Adds even more documentation. [René Samselnig]

- Adds configuration documentation. [René Samselnig]

- Adds code semantics to installation block. [René Samselnig]

- Adds code semantics to installation block. [René Samselnig]

- Adds code semantics to installation block. [René Samselnig]

- Adds code semantics to installation block. [René Samselnig]

- Moves default workflow into base DatabaseConnection class. Adds
  documentation. [René Samselnig]

- Creates a .alfredworkflow installation file. [René Samselnig]

- Adds the ability to use .../table/=searchterm or .../table/~searchterm
  (which searches all fields specified in the search array of the table
  comment). [René Samselnig]

- Fixes workflow. [René Samselnig]

- Completely rewrites the options parsing for each individual driver.
  [René Samselnig]

- Adds command line arguments. [René Samselnig]

- Moves mock source to test sources. [René Samselnig]

- Re-structures tests. [René Samselnig]

- Updates autocomplete strings and expected testcase values. [René
  Samselnig]

- Uses more features from SQLAlchemy. [René Samselnig]

- Adds SQLAlchemy as database layer. [René Samselnig]

- Adds sqlite database driver. [René Samselnig]

- Adds info when table comment is not overly correct. [René Samselnig]

- Adds a mock service to test database abstraction. [René Samselnig]

- Adds more tests. [René Samselnig]

- Makes databaseconnection more flexible. [René Samselnig]

- Makes database sources modular. [René Samselnig]

- Re-organises tests. Puts postgres specific code into the postgresql
  module. [René Samselnig]

- Re-organises into modules. [René Samselnig]

- Re-structures dbnavigator into modules. [René Samselnig]

- Updates icons. [René Samselnig]

- Fixes issues with cache. Default cache time: 2 minutes. [René
  Samselnig]

- Adds first version of foreign key caching. Not yet working correctly.
  [René Samselnig]

- Cleans up Makefile. [René Samselnig]

- Fixes missing localhost entries. [René Samselnig]

- Changes ids to uuids in output. [René Samselnig]

- Fixes missing foreign value entries. [René Samselnig]

- Adds more tests. [René Samselnig]

- Fixes testcase. [René Samselnig]

- Adds more tests. [René Samselnig]

- Fixes failing test. [René Samselnig]

- Adds even more tests. [René Samselnig]

- Adds more tests. [René Samselnig]

- Adds tests. [René Samselnig]

- Cleans up code. Adds different item printers and command line options
  to choose between them (-p: Python, -s: Simple, -x: XML, -j: JSON).
  [René Samselnig]

- Fixes problems with preinstalled python. [René Samselnig]

- Removes unneccesary logging. [René Samselnig]

- Adds the valid attribute to item. [René Samselnig]

- Adds icons. Fixes performance issues. [René Samselnig]

- Adds the ability to filter rows by column_name=value. [René
  Samselnig]

- Adds the ability to filter rows by column_name=value. [René
  Samselnig]

- Code cleanup. [René Samselnig]

- Adds default search columns. [René Samselnig]

- Adds title and subtitle to the list of displayed values of a row.
  [René Samselnig]

- Displays the foreign table title in lists. [René Samselnig]

- Fixes problem with multiple foreign keys to the same table. [René
  Samselnig]

- Uses URIs instead of space delimited arguments. [René Samselnig]

- Uses URIs instead of space delimited arguments. [René Samselnig]

- Updates the README.md. [René Samselnig]

- Is iA Writer able to edit the README.md? [René Samselnig]

- Fixes makefile and SQL error. [René Samselnig]

- Create README.md. [René Samselnig]

  Adds the README.md

- Initial commit. [René Samselnig]


