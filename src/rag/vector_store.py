"""
Vector Store
"""

import json
import sqlite3

from pathlib import Path

DB_PATH = "data/ecommerce.db"


class VectorStore:

    def __init__(self):

        Path("data").mkdir(
            exist_ok=True
        )

        self.conn = sqlite3.connect(
            DB_PATH,
            check_same_thread=False
        )

        self.create_table()

    def create_table(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vectors(
                id INTEGER PRIMARY KEY,
                content TEXT,
                embedding TEXT
            )
            """
        )

        self.conn.commit()

    def add_document(
        self,
        content: str,
        embedding: list
    ):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO vectors(
                content,
                embedding
            )
            VALUES(?,?)
            """,
            (
                content,
                json.dumps(embedding)
            )
        )

        self.conn.commit()

    def get_all_documents(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT content, embedding
            FROM vectors
            """
        )

        return cursor.fetchall()