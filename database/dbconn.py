import sqlite3
from utilities import DB
from pathlib import Path
from typing import Any


def execute_query(
    query: str, params: dict[str, Any] | None = None, db_path: Path = DB
) -> None:
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(query, params or {})
    conn.commit()
    conn.close()


def fetch_result(
    query: str, params: dict[str, Any] | None = None, db_path: Path = DB
) -> list[dict[str, Any]]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute(query, params or {})
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows
