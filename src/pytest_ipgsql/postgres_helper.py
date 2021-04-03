import os

from pathlib import Path
from pytest_ipgsql.parsers.import_parser import ImportParser


class PostgresHelper:

    def __init__(self) -> None:
        """Initialize the class."""

        pass

    @staticmethod
    def exec_sql_file(conn, sql_file_path, global_path) -> None:
        if not Path(sql_file_path).is_file():
            return

        with open(sql_file_path, 'r') as f:
            sql_file_content = f.read()

        sql_commands = sql_file_content.split(';')
        for sql_command in sql_commands:
            sql_command = sql_command.strip()
            if not sql_command:
                continue

            match_type, sql_file = ImportParser.parse(sql_command)
            if match_type == 'local':
                PostgresHelper.exec_sql_file(conn, sql_file, global_path)
            elif match_type == 'global':
                PostgresHelper.exec_sql_file(conn, os.path.join(global_path, sql_file), global_path)
            else:
                with conn.cursor() as cur:
                    cur.execute(sql_command)
                    conn.commit()
