import pytest


@pytest.fixture
def pytester_fixture(pytester):
    def pytester_setup(params):
        pytester.makeconftest(
            """
            pytest_plugins = [
                "src.pytest_pgsqlit.plugin",
            ]        
            """
        )

        pytester.makepyfile(
            f"""
            from unittest.mock import patch
    
            def test__given__fixture__when__testing__then__correct_config(pgm_session_fixture):
                assert pgm_session_fixture.get_config() == {{'dbname': '{params['db_name']}', 'host': '{params['host']}',
                 'password': '{params['password']}', 'port': {params['port']}, 'user': '{params['user']}'}}
                assert pgm_session_fixture.global_fixtures_path == '{params['global_fixtures_path']}'
            """
        )

        return pytester

    return pytester_setup


def test__given__default_input__when__init__then__correct_config(pytester_fixture):
    pytester = pytester_fixture(
        {'db_name': 'test_postgres', 'host': '127.0.0.1', 'password': 'password', 'port': '5432', 'user': 'postgres',
         'global_fixtures_path': 'tests/integration/fixtures/postgres'})

    result = pytester.runpytest()

    result.assert_outcomes(passed=1)


def test__given__ini_input__when__init__then__correct_config(pytester_fixture):
    pytester = pytester_fixture(
        {'db_name': 'test_db', 'host': 'test_host', 'password': 'test_password', 'port': '12345', 'user': 'test_user',
         'global_fixtures_path': 'test_fixture_path'})

    pytester.makefile(".ini", pytest="""
    [pytest]
    postgresql_host=test_host
    postgresql_port=12345
    postgresql_user=test_user
    postgresql_password=test_password
    postgresql_db_name=test_db
    pgsqlit_global_fixtures_path=test_fixture_path
    """)

    result = pytester.runpytest()

    result.assert_outcomes(passed=1)


def test__given__cli_input__when__init__then__correct_config(pytester_fixture):
    pytester = pytester_fixture(
        {'db_name': 'test_db', 'host': 'test_host', 'password': 'test_password', 'port': '12345', 'user': 'test_user',
         'global_fixtures_path': 'test_fixture_path'})

    result = pytester.runpytest("--postgresql-host", "test_host", "--postgresql-port", "12345",
                                "--postgresql-user", "test_user", "--postgresql-password", "test_password",
                                "--postgresql-db-name", "test_db", "--pgsqlit-global-fixtures-path",
                                "test_fixture_path")

    result.assert_outcomes(passed=1)
