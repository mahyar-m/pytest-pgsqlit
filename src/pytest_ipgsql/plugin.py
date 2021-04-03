import pytest

from _pytest.fixtures import FixtureRequest
from pytest_ipgsql.pg_manager import PgManager


def pytest_addoption(parser) -> None:
    """Configure for pytest-ipgsql"""

    parser.addini(
        name='ipgsql_global_fixtures_path',
        default='tests/integration/fixtures/postgres',
        help='',
    )

    parser.addini(
        name='postgresql_host',
        default='127.0.0.1',
        help='',
    )

    parser.addini(
        name='postgresql_port',
        default=None,
        help='',
    )

    parser.addini(
        name='postgresql_user',
        default='postgres',
        help='',
    )

    parser.addini(
        name='postgresql_password',
        default=None,
        help='',
    )

    parser.addini(
        name='postgresql_db_name',
        default=None,
        help='',
    )

    parser.addoption(
        '--ipgsql-global-fixtures-path',
        action='store',
        dest='ipgsql_global_fixtures_path',
    )

    parser.addoption(
        '--postgresql-host',
        action='store',
        dest='postgresql_host',
    )

    parser.addoption(
        '--postgresql-port',
        action='store',
        dest='postgresql_port',
    )

    parser.addoption(
        '--postgresql-user',
        action='store',
        dest='postgresql_user',
    )

    parser.addoption(
        '--postgresql-password',
        action='store',
        dest='postgresql_password',
    )

    parser.addoption(
        '--postgresql-db-name',
        action='store',
        dest='postgresql_db_name',
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
