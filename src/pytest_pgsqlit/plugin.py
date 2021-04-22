import pytest

from _pytest.fixtures import FixtureRequest
from pytest_pgsqlit.pg_manager import PgManager

pytest_options = [
    {
        'name': 'pgsqlit_global_fixtures_path',
        'option': '--pgsqlit-global-fixtures-path',
        'default': 'tests/integration/fixtures/postgres',
        'help': '',
    },
    {
        'name': 'postgresql_host',
        'option': '--postgresql-host',
        'default': '127.0.0.1',
        'help': '',
    },
    {
        'name': 'postgresql_port',
        'option': '--postgresql-port',
        'default': 5432,
        'help': '',
    },
    {
        'name': 'postgresql_user',
        'option': '--postgresql-user',
        'default': 'postgres',
        'help': '',
    },
    {
        'name': 'postgresql_password',
        'option': '--postgresql-password',
        'default': None,
        'help': '',
    },
    {
        'name': 'postgresql_db_name',
        'option': '--postgresql-db-name',
        'default': None,
        'help': '',
    },
]


def pytest_addoption(parser) -> None:
    """Configure for pytest-pgsqlit"""

    for option in pytest_options:
        parser.addini(
            name=option['name'],
            default=option['default'],
            help=option['help'],
        )

        parser.addoption(
            option['option'],
            action='store',
            dest=option['name'],
        )


@pytest.fixture(scope="session")
def pgm_session_fixture(request: FixtureRequest) -> PgManager:
    with PgManager(request) as pg_manager:
        yield pg_manager


@pytest.fixture(scope="class")
def pgm_class_fixture(pgm_session_fixture: PgManager, request: FixtureRequest) -> PgManager:
    pgm_session_fixture.execute_sql_file('setup_class.sql', location='local', request=request)
    yield pgm_session_fixture
    pgm_session_fixture.execute_sql_file('teardown_class.sql', location='local', request=request)


@pytest.fixture(scope="function")
def pgm_function_fixture(pgm_class_fixture: PgManager, request: FixtureRequest) -> PgManager:
    pgm_class_fixture.execute_sql_file('setup_method.sql', location='local', request=request)
    yield pgm_class_fixture
    pgm_class_fixture.execute_sql_file('teardown_method.sql', location='local', request=request)
