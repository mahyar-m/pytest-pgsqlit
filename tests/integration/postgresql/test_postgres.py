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

    def test_example_postgres1(self, pgm_function_fixture, request):
        pgm_function_fixture.execute_sql_file('test_1.sql', request=request, location='local')
        conn = pgm_function_fixture.get_conn()
        cur = conn.cursor()
        cur.execute("select * from test")
        result = cur.fetchall()
        assert result == [(1, 1, 'test'), (2, 1, 'test_1')]

    def test_example_postgres2(self, pgm_function_fixture, request):
        pgm_function_fixture.execute_sql_file('test_2.sql', request=request, location='local')
        conn = pgm_function_fixture.get_conn()
        cur = conn.cursor()
        cur.execute("select * from test")
        result = cur.fetchall()
        assert result == [(1, 1, 'test'), (2, 2, 'test_2')]
