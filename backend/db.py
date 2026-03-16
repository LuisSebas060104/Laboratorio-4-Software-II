import sqlite3

DB_PATH = "tasks.db"


def get_conn():
    """
    Crea una conexión a SQLite y devuelve filas como diccionarios.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """
    Crea la tabla tasks si no existe.
    """
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_code TEXT NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            due_date TEXT NOT NULL,         -- formato: YYYY-MM-DD
            published INTEGER NOT NULL DEFAULT 0,
            created_by TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
        """
    )

    # Índices útiles (mejoran listados por curso y filtros)
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_course ON tasks(course_code);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_published ON tasks(published);")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);")

    conn.commit()
    conn.close()
