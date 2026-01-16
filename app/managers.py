import sqlite3
from models import Actor


class ActorManager:
    def __init__(self, db_name: str, table_name: str):
        self.connection = sqlite3.connect(db_name)
        self.table_name = table_name
        # Optional: Ensure the table exists with correct columns
        self._create_table()

    def _create_table(self):
        """Helper method to ensure the table structure is present."""
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT
        );
        """
        self.connection.execute(query)
        self.connection.commit()

    def create(self, first_name: str, last_name: str) -> None:
        """Creates a new entry in the actor table."""
        query = f"INSERT INTO {self.table_name} (first_name, last_name) VALUES (?, ?)"
        self.connection.execute(query, (first_name, last_name))
        self.connection.commit()

    def all(self) -> list[Actor]:
        """Returns a list of Actor instances from the DB."""
        cursor = self.connection.cursor()
        query = f"SELECT id, first_name, last_name FROM {self.table_name}"
        cursor.execute(query)
        rows = cursor.fetchall()

        return [Actor(id=row[0], first_name=row[1], last_name=row[2]) for row in rows]

    def update(self, pk: int, new_first_name: str, new_last_name: str) -> None:
        """Updates entry with given pk."""
        query = f"UPDATE {self.table_name} SET first_name = ?, last_name = ? WHERE id = ?"
        self.connection.execute(query, (new_first_name, new_last_name, pk))
        self.connection.commit()

    def delete(self, pk: int) -> None:
        """Deletes entry with given pk from DB."""
        query = f"DELETE FROM {self.table_name} WHERE id = ?"
        self.connection.execute(query, (pk,))
        self.connection.commit()