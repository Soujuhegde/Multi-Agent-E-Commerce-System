"""
SQLite Tool
"""

import sqlite3

from typing import Any


class SQLiteTool:

    def __init__(
        self,
        db_path: str
    ):
        self.db_path = db_path

    def execute_query(
        self,
        query: str,
        params: tuple = ()
    ) -> Any:

        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()

        try:

            cursor.execute(
                query,
                params
            )

            conn.commit()

            return cursor.fetchall()

        finally:

            conn.close()

    def execute_insert(
        self,
        query: str,
        params: tuple
    ):

        conn = sqlite3.connect(
            self.db_path
        )

        cursor = conn.cursor()

        try:

            cursor.execute(
                query,
                params
            )

            conn.commit()

            return cursor.lastrowid

        finally:

            conn.close()