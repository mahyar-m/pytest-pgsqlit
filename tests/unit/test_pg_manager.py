from unittest.mock import call

import pytest
from _pytest.fixtures import FixtureRequest
from pytest_pgsqlit.pg_manager import PgManager
from callee import Contains


class TestPgManager:

    @pytest.fixture
    def mock_request(self, mocker):
        mock = mocker.patch("_pytest.fixtures", spec=FixtureRequest)
        mock.config.getoption.side_effect = ['test', 'localhost', '3306', 'user', 'password', 'db_name']
        return mock

    @pytest.fixture
    def mock_psycopg2_connect(self, mocker):
        return mocker.patch("psycopg2.connect")

    def test__given__request__when__enter_manger__then__setup_correctly(self, mock_request, mock_psycopg2_connect):
        with PgManager(mock_request):
            mock_psycopg2_connect.assert_has_calls([call(host='localhost', port='3306', user='user',
                                                         password='password'),
                                                    call(dbname='db_name', user='user', password='password',
                                                         host='localhost', port='3306')], any_order=True)

            assert mock_psycopg2_connect.return_value.set_isolation_level.call_count == 2
            mock_psycopg2_connect.return_value.cursor.return_value.__enter__.return_value.execute.assert_has_calls(
                [call('DROP DATABASE IF EXISTS "db_name";'), call('CREATE DATABASE "db_name";')])

    def test__given__request__when__exit_manger__then__teardown_correctly(self, mock_request, mock_psycopg2_connect):
        with PgManager(mock_request):
            pass

        cursor = mock_psycopg2_connect.return_value.cursor.return_value.__enter__.return_value.execute
        cursor.assert_any_call(
            Contains('UPDATE pg_database'), ('db_name',))
        cursor.assert_any_call(
            Contains('SELECT pg_terminate_backend'), ('db_name',))
        cursor.assert_any_call(
            Contains('DROP DATABASE IF EXISTS db_name'))

    def test__given__request__when__get_conn__then__return_correct_conn(self, mock_request, mock_psycopg2_connect):
        with PgManager(mock_request) as sut:
            assert sut.get_conn()
