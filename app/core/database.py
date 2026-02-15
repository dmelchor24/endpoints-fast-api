import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Configuración de la base de datos
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATABASE = BASE_DIR / "tasks.db"

# Configuración optimizada para concurrencia
def configure_connection(conn):
    """Aplica configuraciones de rendimiento a la conexión"""
    conn.execute('PRAGMA journal_mode=WAL')       # Write-Ahead Logging
    conn.execute('PRAGMA synchronous=NORMAL')     # Balance seguridad/rendimiento
    conn.execute('PRAGMA cache_size=10000')       # ~40MB de cache
    conn.execute('PRAGMA temp_store=MEMORY')      # Operaciones temp en RAM
    conn.execute('PRAGMA busy_timeout=5000')      # Espera 5s antes de timeout
    conn.row_factory = sqlite3.Row
    return conn

# Context manager para obtener una conexión a la base de datos
@contextmanager
def get_db():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn = configure_connection(conn)
    try:
        yield conn
        conn.commit()  # Auto-commit al salir exitosamente
    except Exception:
        conn.rollback()  # Rollback en caso de error
        raise
    finally:
        conn.close()

# Inicializa la base de datos y crea las tablas necesarias
def init_db():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn = configure_connection(conn)
    try:
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
        
        # Crear índices para mejorar el rendimiento
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_created_at 
            ON tasks(created_at)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_tasks_title 
            ON tasks(title)
        """)
        
        conn.commit()
        print(f"✅ Base de datos inicializada con WAL mode")
        print(f"📁 Ubicación: {DATABASE}")
    finally:
        conn.close()