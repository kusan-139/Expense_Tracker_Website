from flask import Flask, request, jsonify
import sqlite3
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "expenses.db")

# Add project root to path so src.database imports work when running directly
sys.path.insert(0, BASE_DIR)

print("API DB Path:", DB_NAME)
app = Flask(__name__)

from src.database import create_table, insert_transaction

create_table()

# ---------------------------
# API Route
# ---------------------------
@app.route("/add", methods=["POST"])
def add_transaction():

    data = request.json

    category = data.get("category")
    amount = data.get("amount")
    type_ = data.get("type", "Expense")
    device_date = data.get("date")
    device_name = data.get("device", "ESP32")

    if not category or not amount:
        return jsonify({"error": "Missing fields"}), 400

    # Use database.py's insert_transaction so that it syncs with SQLite and CSV
    description = f"{device_name} WiFi Entry"
    insert_transaction(device_date, category, description, float(amount), type_)

    return jsonify({"status": "success"}), 200


@app.route("/")
def home():
    return "Expense Tracker IoT API Running"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)