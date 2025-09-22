import sqlite3


def column_exists(cur: sqlite3.Cursor, table: str, column: str) -> bool:
    cur.execute(f"PRAGMA table_info({table})")
    return any(row[1] == column for row in cur.fetchall())


def add_column_if_missing(cur: sqlite3.Cursor, table: str, column_name: str, column_def: str) -> None:
    if column_exists(cur, table, column_name):
        print(f"Column '{column_name}' already exists on '{table}', skipping")
        return
    sql = f"ALTER TABLE {table} ADD COLUMN {column_name} {column_def}"
    print(f"Applying: {sql}")
    cur.execute(sql)


if __name__ == "__main__":
    # Use INTEGER for booleans in SQLite (0/1)
    with sqlite3.connect("travel.db") as con:
        cur = con.cursor()
        # Ensure foreign keys are on (not required for ALTER, but good practice if future ops rely on it)
        cur.execute("PRAGMA foreign_keys = ON")

        add_column_if_missing(cur, "customers", "verified", "INTEGER DEFAULT 0")
        add_column_if_missing(cur, "customers", "verification_code", "TEXT DEFAULT ''")
        add_column_if_missing(cur, "customers", "code_expiry", "DATETIME DEFAULT NULL")

        con.commit()
        print("Migration completed.")