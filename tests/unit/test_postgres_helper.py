import pytest

from unittest.mock import mock_open, patch, MagicMock
from pytest_pgsqlit.postgres_helper import PostgresHelper


class TestPostgresHelper:

    @pytest.fixture
    def mock_path_is_file(self, mocker):
        mock = mocker.patch("pathlib.Path.is_file")
        mock.return_value = True

        return mock

    @pytest.fixture
    def mock_conn(self, mocker):
        return mocker.MagicMock()

    def test__given__non_exist_path__when__exec_sql_file__then__no_execution(self, mock_path_is_file, mock_conn):
        mock_path_is_file.return_value = False
        with patch('builtins.open', read_data="") as mock:
            PostgresHelper.exec_sql_file(mock_conn, "non_exist_path", "global_path")

            assert mock.call_count == 0

    def test__given__simple_sql__when__exec_sql_file__then__execute_correctly(self, mock_path_is_file, mock_conn):
        with patch('builtins.open', mock_open(read_data="SELECT 1;")) as mock:
            PostgresHelper.exec_sql_file(mock_conn, "a_path", "global_path")

            assert mock.call_count == 1
            mock_conn.cursor.return_value.__enter__().execute.assert_called_with('SELECT 1')
            assert mock_conn.commit.call_count == 1

    def test__given__local_import__when__exec_sql_file__then__execute_correctly(self, mock_path_is_file, mock_conn):
        with patch('builtins.open') as mock:
            handle1 = MagicMock()
            handle1.__enter__.return_value.read.return_value = "IMPORT test.sql;"
            handle1.__exit__.return_value = False
            handle2 = MagicMock()
            handle2.__enter__.return_value.read.return_value = "SELECT 1;"
            handle2.__exit__.return_value = False
            mock.side_effect = (handle1, handle2)

            PostgresHelper.exec_sql_file(mock_conn, "a_path", "global_path")

            assert mock.call_count == 2
            mock.assert_called_with('test.sql', 'r')
            mock_conn.cursor.return_value.__enter__().execute.assert_called_with('SELECT 1')
            assert mock_conn.commit.call_count == 1

    def test__given__global_import__when__exec_sql_file__then__execute_correctly(self, mock_path_is_file, mock_conn):
        with patch('builtins.open') as mock:
            handle1 = MagicMock()
            handle1.__enter__.return_value.read.return_value = "IMPORT_GLOBAL test.sql;"
            handle1.__exit__.return_value = False
            handle2 = MagicMock()
            handle2.__enter__.return_value.read.return_value = "SELECT 1;"
            handle2.__exit__.return_value = False
            mock.side_effect = (handle1, handle2)

            PostgresHelper.exec_sql_file(mock_conn, "a_path", "global_path")

            assert mock.call_count == 2
            mock.assert_called_with('global_path/test.sql', 'r')
            mock_conn.cursor.return_value.__enter__().execute.assert_called_with('SELECT 1')
            assert mock_conn.commit.call_count == 1
