import sqlite3
from realty_redux.common.sql.BaseConnector import BaseConnector
from typing import Self

class SQLiteConnector(BaseConnector):
    def __init__(self, location: str):
        self.db_location: str
        self.connection: sqlite3.Connection
        self.cursor: sqlite3.Cursor

        self.init_db(location)

    def __del__(self):
        try:
            self.close_connection()
        except Exception:
            pass

    def init_db(self, location: str) -> Self:
        self.db_location = location
        return self

    def get_connection(self) -> Self:
        self.connection = sqlite3.connect(self.db_location)
        self.cursor = self.connection.cursor()
        return self

    def close_connection(self) -> Self:
        self.connection.close()
        return self

