"""
Custom Turso/libSQL backend for Django using libsql_experimental.
"""
import re
import sqlite3
from collections.abc import Mapping
from datetime import date, datetime, time
from decimal import Decimal

import libsql_experimental
from django.core.exceptions import ImproperlyConfigured
from django.db.backends.sqlite3 import base as sqlite3_base
from django.db.backends.sqlite3.features import DatabaseFeatures as SQLiteFeatures
from django.utils.regex_helper import _lazy_re_compile

FORMAT_QMARK_REGEX = _lazy_re_compile(r"(?<!%)%s")
PYFORMAT_REGEX = re.compile(r"%\(([^)]+)\)s")
ALLOWED_CONNECT_OPTIONS = {
    "auth_token",
    "sync_url",
    "sync_interval",
    "encryption_key",
    "isolation_level",
    "check_same_thread",
    "uri",
}


def adapt_param(param):
    if isinstance(param, datetime):
        return param.isoformat(" ")
    if isinstance(param, date):
        return param.isoformat()
    if isinstance(param, time):
        return param.isoformat()
    if isinstance(param, Decimal):
        return str(param)
    if isinstance(param, bool):
        return int(param)
    return param


def convert_query(query):
    return FORMAT_QMARK_REGEX.sub("?", query).replace("%%", "%")


def convert_mapping_query_and_params(query, params):
    names = PYFORMAT_REGEX.findall(query)
    if names:
        converted_query = PYFORMAT_REGEX.sub("?", query).replace("%%", "%")
        converted_params = tuple(adapt_param(params[name]) for name in names)
        return converted_query, converted_params
    converted_query = convert_query(query)
    converted_params = tuple(adapt_param(value) for value in params.values())
    return converted_query, converted_params


class TursoCursor:
    """Cursor wrapper that converts Django placeholders to SQLite qmark style."""

    def __init__(self, cursor):
        self._cursor = cursor

    def execute(self, sql, params=None):
        if params is None:
            return self._cursor.execute(convert_query(sql))
        if isinstance(params, Mapping):
            converted_sql, converted_params = convert_mapping_query_and_params(sql, params)
            return self._cursor.execute(converted_sql, converted_params)
        converted_sql = convert_query(sql)
        converted_params = tuple(adapt_param(param) for param in params)
        return self._cursor.execute(converted_sql, converted_params)

    def executemany(self, sql, param_list):
        for params in param_list:
            self.execute(sql, params)
        return self

    def __getattr__(self, name):
        return getattr(self._cursor, name)

    def __iter__(self):
        return iter(self._cursor)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


class Database:
    """sqlite3-compatible module facade backed by libsql_experimental."""

    connect = staticmethod(libsql_experimental.connect)
    PARSE_DECLTYPES = sqlite3.PARSE_DECLTYPES
    PARSE_COLNAMES = sqlite3.PARSE_COLNAMES
    Error = sqlite3.Error
    DatabaseError = sqlite3.DatabaseError
    IntegrityError = sqlite3.IntegrityError
    ProgrammingError = sqlite3.ProgrammingError
    OperationalError = sqlite3.OperationalError
    NotSupportedError = sqlite3.NotSupportedError
    InterfaceError = sqlite3.InterfaceError
    InternalError = sqlite3.InternalError
    DataError = sqlite3.DataError
    Warning = sqlite3.Warning
    sqlite_version_info = sqlite3.sqlite_version_info
    sqlite_version = sqlite3.sqlite_version
    register_converter = staticmethod(sqlite3.register_converter)
    register_adapter = staticmethod(sqlite3.register_adapter)


class DatabaseFeatures(SQLiteFeatures):
    # libsql_experimental does not provide sqlite3's transaction semantics for DDL.
    can_rollback_ddl = False
    supports_atomic_references_rename = False


class DatabaseWrapper(sqlite3_base.DatabaseWrapper):
    vendor = "sqlite"
    display_name = "Turso (libSQL)"
    Database = Database
    features_class = DatabaseFeatures

    def get_connection_params(self):
        settings_dict = self.settings_dict
        if not settings_dict["NAME"]:
            raise ImproperlyConfigured(
                "settings.DATABASES is improperly configured. Please supply the NAME value."
            )
        params = {
            "database": settings_dict["NAME"],
            "check_same_thread": False,
            "uri": True,
            "isolation_level": None,
        }
        options = settings_dict.get("OPTIONS", {})
        for key, value in options.items():
            if key in ALLOWED_CONNECT_OPTIONS:
                params[key] = value
        return params

    def get_new_connection(self, conn_params):
        conn = libsql_experimental.connect(**conn_params)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def create_cursor(self, name=None):
        return TursoCursor(self.connection.cursor())

    def _set_autocommit(self, autocommit):
        # libsql_experimental exposes isolation_level as read-only.
        return

    def _close(self):
        if self.connection is not None and hasattr(self.connection, "close"):
            self.connection.close()

    def is_usable(self):
        if self.connection is None:
            return False
        try:
            self.connection.execute("SELECT 1")
            return True
        except Exception:
            return False

    def disable_constraint_checking(self):
        # libsql_experimental does not allow toggling this pragma in Django's flow.
        return True

    def enable_constraint_checking(self):
        return

    def check_constraints(self, table_names=None):
        return
