import sqlite3
import os
from datetime import datetime

DB_PATH = "data/bookings.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            username TEXT,
            time TEXT NOT NULL,
            date TEXT NOT NULL
        )
        """)
        conn.commit()

def get_available_slots(date):
    all_slots = ["10:00", "11:00", "12:00", "14:00", "15:00", "16:00"]
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT time FROM bookings WHERE date = ?", (date,))
        booked = [row[0] for row in cursor.fetchall()]
    return [slot for slot in all_slots if slot not in booked]

def book_slot(user_id, username, time, date):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO bookings (user_id, username, time, date)
        VALUES (?, ?, ?, ?)
        """, (user_id, username, time, date))
        conn.commit()

def get_bookings_by_date(date):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT username, time FROM bookings WHERE date = ?", (date,))
        return cursor.fetchall()