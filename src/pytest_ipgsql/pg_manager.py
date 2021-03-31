import os

import psycopg2

from types import TracebackType
from typing import TypeVar, Optional, Type

from _pytest.fixtures import FixtureRequest
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from psycopg2._psycopg import cursor, connection

from pytest_ipgsql.postgres_helper import PostgresHelper

PgManagerType = TypeVar("PgManagerType", bound="PgManager")


class PgManager:
    """Class to manage the creation of the test database and handle the connection"""

    def __init__(
            self,
            request: FixtureRequest
    ) -> None:
        """Initialize the class."""

        self.request = request
        self.conn = None
        self._internal_conn = None

        self.user = None
        self.password = None
        self.host = None
        self.port = None
        self.db_name = None
        self.global_fixtures_path = None

    def init(self) -> None:
        """Create database in postgresql."""
        self.init_config()

        self._internal_conn = psycopg2.connect(
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self._internal_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        with self._internal_conn.cursor() as cur:
            cur.execute('DROP DATABASE IF EXISTS "{}";'.format(self.db_name))
            cur.execute('CREATE DATABASE "{}";'.format(self.db_name))

        self.conn = psycopg2.connect(
            dbname=self.db_name,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)


    def init_config(self) -> None:
        """Initialize the class attributes with config options."""

        for option in ['global_fixtures_path']:
            option_name = 'ipgsql_' + option
            setattr(self, option, self.request.config.getoption(option_name) or self.request.config.getini(option_name))

        for option in ['host', 'port', 'user', 'password', 'db_name']:
            option_name = 'postgresql_' + option
            setattr(self, option, self.request.config.getoption(option_name) or self.request.config.getini(option_name))

    def drop(self) -> None:
        """Drop the database"""

        with self._internal_conn.cursor() as cur:
            cur.execute('UPDATE pg_database SET datallowconn=false WHERE datname = %s;', (self.db_name,))
            cur.execute(
                """
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                    FROM pg_stat_activity
                    WHERE pg_stat_activity.datname = %s;
                """,
                (self.db_name,))
            cur.execute('DROP DATABASE IF EXISTS "{}";'.format(self.db_name))

    def get_conn(self) -> connection:
        """Return a connection"""

        return self.conn

    def execute_sql_file(self, sql_file_path, location=None, request=None, local_path=None, global_path=None) -> None:
        if location == 'local':
            if not local_path:
                local_path = os.path.join(request.fspath.dirname, 'fixtures', 'postgres')
            sql_file_path = os.path.join(local_path, sql_file_path)
        elif location == 'global':
            # TODO implement
            pass
        elif location == 'relative':
            # TODO implement
            pass

        if not global_path:
            global_path = os.path.join(self.global_fixtures_path)

        PostgresHelper.exec_sql_file(self.get_conn(), sql_file_path, global_path)

    def __enter__(self):
        self.init()
        return self

    def __exit__(self: PgManagerType,
                 exc_type: Optional[Type[BaseException]],
                 exc_val: Optional[BaseException],
                 exc_tb: Optional[TracebackType]) -> None:
        self.drop()
        self.conn.close()
