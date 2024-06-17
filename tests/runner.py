"""Test database runner module."""
from types import MethodType
from typing import Any

from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.test.runner import DiscoverRunner


def prepare_db(self):
    """Prepare database schema.

    Args:
        self: self class.
    """
    self.connect()
    self.connection.cursor().execute('CREATE SCHEMA IF NOT EXISTS crud_api;')


class PostgresSchemaRunner(DiscoverRunner):
    """PSQL runner class.

    Args:
        DiscoverRunner: a Django test runner that uses unittest2 test discovery.
    """

    def setup_databases(self, **kwargs: Any) -> list[tuple[BaseDatabaseWrapper, str, bool]]:
        """Set up database connection.

        Args:
            kwargs: keyword arguments.

        Returns:
            list[tuple[BaseDatabaseWrapper, str, bool]]: represent a database connection.
        """
        for conn_name in connections:
            connection = connections[conn_name]
            connection.prepare_database = MethodType(prepare_db, connection)
        return super().setup_databases(**kwargs)
