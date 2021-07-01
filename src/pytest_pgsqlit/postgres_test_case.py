import unittest
import pytest

from pytest_pgsqlit.pg_manager import PgManager


class PostgresTestCase(unittest.TestCase):

    @pytest.fixture(autouse=True)
    def init_conn(self, pgm_function_fixture: PgManager) -> None:
        self.pg_manager = pgm_function_fixture

    def assertRowCount(self, full_table_name: str = None, expected_count: int = None) -> None:
        with self.pg_manager.get_conn().cursor() as cur:
            cur.execute("SELECT count(*) from {}".format(full_table_name))
            result = cur.fetchone()

        self.assertEqual(expected_count, result[0])

    def assertSqlResult(self, sql: str = "", expected_result: [] = None, sql_params: tuple = None) -> None:
        with self.pg_manager.get_conn().cursor() as cur:
            cur.execute(sql, sql_params)
            result = cur.fetchall()

        self.assertEqual(expected_result, result)
