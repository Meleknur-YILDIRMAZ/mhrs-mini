import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("mhrs.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS patients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        tc TEXT NOT NULL UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_tc TEXT NOT NULL,
        doctor TEXT NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()