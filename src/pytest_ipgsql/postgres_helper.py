import os

from pathlib import Path
from _pytest.fixtures import FixtureRequest

from pytest_ipgsql.parsers.import_parser import ImportParser


class PostgresHelper:

    def __init__(self):
        pass

    @staticmethod
    def exec(conn, request: FixtureRequest, sql_file_name):
        fixture_root_folder = os.path.join(request.config.invocation_dir, request.config.inicfg['testpaths'],
                                           'fixtures', 'postgres')
        sql_file_path = os.path.join(request.fspath.dirname, 'fixtures', 'postgres', sql_file_name)

        PostgresHelper.exec_sql_file(sql_file_path, conn, fixture_root_folder)

    @staticmethod
    def exec_sql_file(sql_file_path, conn, fixture_root_folder):
        if not Path(sql_file_path).is_file():
            return

        with open(sql_file_path, 'r') as f:
            sql_file_content = f.read()

        sql_commands = sql_file_content.split(';')
        for sql_command in sql_commands:
            sql_command = sql_command.strip()
            if not sql_command:
                continue

            if ImportParser.is_import(sql_command):
                file = ImportParser.parse(sql_command)
                PostgresHelper.exec_sql_file(os.path.join(fixture_root_folder, file), conn, fixture_root_folder)
                continue

            with conn.cursor() as cur:
                cur.execute(sql_command)
                conn.commit()
