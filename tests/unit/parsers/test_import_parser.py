import pytest

from pytest_pgsqlit.parsers.import_parser import ImportParser


class TestImportParser:

    test_data = [
        ("IMPORT_GLOBAL test_table.sql;", "global", "test_table.sql;"),
        ("IMPORT test_table.sql;", "local", "test_table.sql;"),
        ("test_table.sql;", None, "test_table.sql;"),
    ]

    @pytest.mark.parametrize("import_sql,expected_scope,expected_sql", test_data)
    def test__given__different_sql__when__parse__then__parse_correct_sql(self, import_sql, expected_scope,
                                                                         expected_sql):
        sut = ImportParser()
        scope, sql = sut.parse(import_sql)

        assert scope == expected_scope
        assert sql == expected_sql
