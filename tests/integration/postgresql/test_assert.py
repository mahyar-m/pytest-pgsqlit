from pytest_pgsqlit.postgres_test_case import PostgresTestCase


class TestAssert(PostgresTestCase):

    def test_assertRowCount(self):
        self.assertRowCount(full_table_name='public.table_1', expected_count=1)

    def test_assertSqlResult(self):
        self.assertSqlResult(sql="SELECT * from public.table_1 where num=%s", expected_result=[(1, 1, 'test_1')],
                             sql_params=(1,))
