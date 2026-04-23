import serial
import sqlite3
from datetime import datetime
import time

DB_NAME = "expenses.db"


# ----------------------------
# Create Table If Not Exists
# ----------------------------
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            category TEXT,
            description TEXT,
            amount REAL,
            type TEXT
        )
    """)

    conn.commit()
    conn.close()


# ----------------------------
# Insert Transaction
# ----------------------------
def insert_transaction(category, amount, type_):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO transactions (date, category, description, amount, type)
        VALUES (?, ?, ?, ?, ?)
    """, (
        datetime.now(),
        category,
        "ESP32 Auto Entry",
        float(amount),
        type_
    ))

    conn.commit()
    conn.close()


# ----------------------------
# Reset All Records
# ----------------------------
def reset_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM transactions")

    conn.commit()
    conn.close()
    print("Database Reset Successfully")


# ----------------------------
# Start Serial Listener
# ----------------------------
def start_listener(port="COM3", baudrate=115200):

    create_table()

    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"Listening to ESP32 on {port}...")

    except Exception as e:
        print(f"Error opening serial port: {e}")
        return

    while True:
        try:
            if ser.in_waiting:
                line = ser.readline().decode("utf-8").strip()
                print(f"Received: {line}")

                # Handle RESET signal
                if line == "RESET":
                    reset_database()
                    continue

                # Handle CSV formatted data
                if "," in line:
                    parts = line.split(",")

                    if len(parts) == 3:
                        category, amount, type_ = parts
                        insert_transaction(category, amount, type_)
                        print(f"Inserted: {category} - {amount}")

        except Exception as e:
            print(f"Error processing data: {e}")

        time.sleep(0.1)


if __name__ == "__main__":
    start_listener(port="COM3")