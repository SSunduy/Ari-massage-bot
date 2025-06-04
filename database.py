import requests
from config import SUPABASE_URL, SUPABASE_KEY

TABLE_NAME = "bookings"

HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation"
}

def init_db():
    # В Supabase таблица создаётся через интерфейс
    pass

def get_available_slots(date):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?select=time&date=eq.{date}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        booked = [item["time"] for item in response.json()]
        all_slots = ["10:00", "11:00", "12:00", "14:00", "15:00", "16:00"]
        return [slot for slot in all_slots if slot not in booked]
    return []

def book_slot(user_id, username, time, date):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}"
    data = {
        "user_id": user_id,
        "username": username,
        "time": time,
        "date": date
    }
    response = requests.post(url, headers=HEADERS, json=data)
    return response.status_code == 201

def get_bookings_by_date(date):
    url = f"{SUPABASE_URL}/rest/v1/{TABLE_NAME}?select=username,time&date=eq.{date}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return [(item["username"], item["time"]) for item in response.json()]
    return []