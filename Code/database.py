import sqlite3

DB_PATH = "sparkline_demo.db"


def get_connection():
    """
    Create and return a SQLite connection.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_schema():
    """
    Extract database schema dynamically.
    This schema will be provided to Gemini.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
    """)

    tables = cursor.fetchall()

    schema_text = ""

    for table in tables:
        table_name = table["name"]

        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = cursor.fetchall()

        schema_text += f"\nTable: {table_name}\n"

        for column in columns:
            schema_text += (
                f"- {column['name']} ({column['type']})\n"
            )

    conn.close()

    return schema_text.strip()


def execute_query(sql_query):
    """
    Execute validated SQL query and return results.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(sql_query)

    rows = cursor.fetchall()

    result = [dict(row) for row in rows]

    conn.close()

    return result