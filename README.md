# pytest-pgsqlit

[![PyPI version][]][1]

[![Python versions][]][1]

[![See Build Status on Travis CI][]][2]

[![See Build Status on AppVeyor][]][3]

PostgreSQL Integration Test in Python

## Features

-   Easy integration test
-   Session/Class/Function level fixtures

## Requirements

-   psycopg2
-   PostgresSQL

## Installation

You can install "pytest-pgsqlit" via [pip][] from [PyPI][]:

    $ pip install pytest-pgsqlit

## Setup

This pluging uses pytest.ini or the option that passes to the pytest
to configure the connection to database and also find the path to 
the global fixtures.

A sample pytest.ini:
```
testpaths =
    tests/integration
postgresql_host=127.0.0.1
postgresql_port=5432
postgresql_user=postgres
postgresql_password=password
postgresql_db_name=test_integration
ipgsql_global_fixtures_path=tests/integration/fixtures/postgres
```
Or command line option:
```
--postgresql-host 127.0.0.1
...
```


## Usage

This plugin contains different fixtures to help setup and 
teardown the PostgreSQL database. Each of these will put 
the database in a proper state for the test function.

- pgm_session_fixture:
- pgm_class_fixture:
- pgm_function_fixture:


## Contributing

Contributions are very welcome. Tests can be run with [tox][], please
ensure the coverage at least stays the same before you submit a pull
request.

## License

Distributed under the terms of the [MIT][] license, "pytest-pgsqlit" is
free and open source software

## Issues

If you encounter any problems, please [file an issue][] along with a
detailed description.

  [PyPI version]: https://img.shields.io/pypi/v/pytest-ipgsql.svg
  [1]: https://pypi.org/project/pytest-ipgsql
  [Python versions]: https://img.shields.io/pypi/pyversions/pytest-ipgsql.svg
  [See Build Status on Travis CI]: https://travis-ci.org/mahyar-m/pytest-ipgsql.svg?branch=master
  [2]: https://travis-ci.org/mahyar-m/pytest-ipgsql
  [See Build Status on AppVeyor]: https://ci.appveyor.com/api/projects/status/github/mahyar-m/pytest-ipgsql?branch=master
  [3]: https://ci.appveyor.com/project/mahyar-m/pytest-ipgsql/branch/master
  [pytest]: https://github.com/pytest-dev/pytest
  [Cookiecutter]: https://github.com/audreyr/cookiecutter
  [@hackebrot]: https://github.com/hackebrot
  [cookiecutter-pytest-plugin]: https://github.com/pytest-dev/cookiecutter-pytest-plugin
  [pip]: https://pypi.org/project/pip/
  [PyPI]: https://pypi.org/project
  [tox]: https://tox.readthedocs.io/en/latest/
  [MIT]: http://opensource.org/licenses/MIT
  [file an issue]: https://github.com/mahyar-m/pytest-ipgsql/issues