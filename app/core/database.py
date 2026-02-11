import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Configuración de la base de datos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE = BASE_DIR / "tasks.db"

# Context manager para obtener una conexión a la base de datos
@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

# Inicializa la base de datos y crea las tablas necesarias
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        conn.commit()