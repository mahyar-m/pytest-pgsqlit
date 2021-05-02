import os


class TestPostgres:

    @classmethod
    def setup_class(cls):
        """ setup any state specific to the execution of the given class (which
        usually contains tests).
        """

    @classmethod
    def teardown_class(cls):
        """ teardown any state that was previously setup with a call to
        setup_class.
        """

    def setup_method(self, method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """

    def teardown_method(self, method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """

    def test_global_and_local_import_works(self, pgm_function_fixture):
        conn = pgm_function_fixture.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT 'public.table_1'::regclass, 'public.table_2'::regclass")

        assert cur.fetchone() == ('table_1', 'table_2')

    def test_setup_method_sql_executed(self, pgm_function_fixture):
        conn = pgm_function_fixture.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * from public.table_1")
        result = cur.fetchall()

        assert result == [(1, 1, 'test_1')]

    def test_execute_sql_file_on_local_sql(self, pgm_function_fixture, request):
        pgm_function_fixture.execute_sql_file('insert_table_2.sql', request=request, location='local')

        conn = pgm_function_fixture.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * from public.table_2")
        result = cur.fetchall()

        assert result == [(1, 2, 'test_2')]

    def test_execute_sql_file_on_global_sql(self, pgm_function_fixture, request):
        pgm_function_fixture.execute_sql_file('insert_table_1.sql', request=request, location='global')

        conn = pgm_function_fixture.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * from public.table_1")
        result = cur.fetchall()

        assert result == [(1, 1, 'test_1'), (2, 1, 'test_global')]

    def test_execute_sql_file_on_relative_sql(self, pgm_function_fixture, request):
        sql_path = os.path.join('fixtures', 'postgres', 'insert_table_1.sql')
        pgm_function_fixture.execute_sql_file(sql_path, request=request, location='relative')

        conn = pgm_function_fixture.get_conn()
        cur = conn.cursor()
        cur.execute("SELECT * from public.table_1")
        result = cur.fetchall()

        assert result == [(1, 1, 'test_1'), (2, 1, 'test_1')]
