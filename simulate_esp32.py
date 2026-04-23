import requests
import time
import random
from datetime import datetime, timedelta

URL = "http://127.0.0.1:5000/add"

categories = [
    ("Food", "Expense"),
    ("Travel", "Expense"),
    ("Shopping", "Expense"),
    ("Bills", "Expense"),
    ("Rent", "Expense"),
    ("Salary", "Income"),
    ("Bonus", "Income"),
    ("Investment", "Income")
]

devices = [
    "ESP32-01",
    "ESP32-02",
    "ESP32-Kitchen",
    "ESP32-Office",
    "ESP32-Home"
]

def random_date():
    # random date within last 60 days
    days_back = random.randint(0, 60)
    random_day = datetime.now() - timedelta(days=days_back)
    return random_day.strftime("%d-%m-%Y"), random_day.month

while True:
    category, type_ = random.choice(categories)
    device = random.choice(devices)

    # random realistic amount
    if type_ == "Expense":
        amount = random.randint(50, 5000)
    else:
        amount = random.randint(5000, 50000)

    date_str, month = random_date()

    data = {
        "category": category,
        "amount": amount,
        "type": type_,
        "date": date_str,
        "month": month,
        "device": device
    }

    try:
        response = requests.post(URL, json=data)
        print("Sent:", data, "| Status:", response.status_code)
    except Exception as e:
        print("Error:", e)

    time.sleep(3)