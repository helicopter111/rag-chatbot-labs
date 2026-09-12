"""Postgres connection helpers.

psycopg is the Python driver (the library that speaks Postgres).
pgvector's register_vector lets us pass Python lists as `vector` values.
"""

from __future__ import annotations

import psycopg
from pgvector.psycopg import register_vector

from config import BACKEND_DIR, DATABASE_URL


def get_conn() -> psycopg.Connection:
    conn = psycopg.connect(DATABASE_URL)
    register_vector(conn)
    return conn


def init_schema() -> None:
    sql = (BACKEND_DIR / "schema.sql").read_text(encoding="utf-8")
    with psycopg.connect(DATABASE_URL, autocommit=True) as conn:
        conn.execute(sql)
