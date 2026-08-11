import sqlite3
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "test_nexus.db"))


class DatabaseManager:
    """
    Maneja la capa de persistencia local usando SQLite.
    Soporta operaciones CRUD y tabla de caché para resiliencia API.
    """

    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        """Crea las tablas necesarias si no existen."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    sku TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    category TEXT DEFAULT 'General',
                    stock INTEGER DEFAULT 0,
                    price REAL DEFAULT 0.0,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_cache (
                    endpoint TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    cached_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()

    # --- OPERACIONES CRUD ---

    def create_product(self, sku: str, name: str, category: str, stock: int, price: float) -> Optional[int]:
        query = "INSERT INTO products (sku, name, category, stock, price) VALUES (?, ?, ?, ?, ?)"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (sku, name, category, stock, price))
            conn.commit()
            return cursor.lastrowid

    def get_all_products(self) -> List[Dict[str, Any]]:
        query = "SELECT id, sku, name, category, stock, price FROM products ORDER BY id DESC"
        with self._get_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            rows = cursor.execute(query).fetchall()
            return [dict(row) for row in rows]

    def update_stock(self, product_id: int, new_stock: int) -> bool:
        query = "UPDATE products SET stock = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (new_stock, product_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_product(self, product_id: int) -> bool:
        query = "DELETE FROM products WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (product_id,))
            conn.commit()
            return cursor.rowcount > 0

    # --- CACHÉ DE RESILIENCIA ---

    def save_cache(self, endpoint: str, payload_json: str):
        query = "INSERT OR REPLACE INTO api_cache (endpoint, payload, cached_at) VALUES (?, ?, CURRENT_TIMESTAMP)"
        with self._get_connection() as conn:
            conn.execute(query, (endpoint, payload_json))
            conn.commit()

    def get_cache(self, endpoint: str) -> Optional[str]:
        query = "SELECT payload FROM api_cache WHERE endpoint = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            row = cursor.execute(query, (endpoint,)).fetchone()
            return row[0] if row else None