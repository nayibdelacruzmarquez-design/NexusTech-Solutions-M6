import unittest
import os
import sqlite3
from src.data.database import DatabaseManager

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        self.db_name = "test_temp.db"
        self.db = DatabaseManager(db_path=self.db_name)

    def tearDown(self):
        # Cerramos conexiones pendientes antes de borrar el archivo en Windows
        del self.db
        if os.path.exists(self.db_name):
            try:
                os.remove(self.db_name)
            except PermissionError:
                pass

    def test_tables_creation(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products';")
        table_products = cursor.fetchone()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='api_cache';")
        table_cache = cursor.fetchone()
        conn.close()

        self.assertIsNotNone(table_products)
        self.assertIsNotNone(table_cache)

if __name__ == "__main__":
    unittest.main()