import sqlite3
import pandas as pd

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_NAME = os.path.join(BASE_DIR, "expenses.db")
print("Streamlit DB Path:", DB_NAME)

def create_connection():
    return sqlite3.connect(DB_NAME)

def create_table():
    conn = create_connection()
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

def insert_transaction(date, category, description, amount, type_):
    # ---- Save to Database ----
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO transactions (date, category, description, amount, type)
        VALUES (?, ?, ?, ?, ?)
    """, (date, category, description, amount, type_))
    conn.commit()
    conn.close()

    # ---- Also Append to CSV ----
    csv_path = os.path.join(BASE_DIR, "data", "expenses.csv")
    new_row = pd.DataFrame([{
        "date": date,
        "category": category,
        "description": description,
        "amount": amount,
        "type": type_
    }])

    try:
        existing_df = pd.read_csv(csv_path)
        existing_df.columns = existing_df.columns.str.lower()
        updated_df = pd.concat([existing_df, new_row], ignore_index=True)
        updated_df.to_csv(csv_path, index=False)
    except FileNotFoundError:
        new_row.to_csv(csv_path, index=False)

def get_data():
    conn = create_connection()
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()
    return df

def load_csv_to_db(csv_path):
    conn = create_connection()
    existing = pd.read_sql_query("SELECT COUNT(*) as count FROM transactions", conn)
    
    if existing["count"][0] > 0:
        print("Database already contains data. Skipping load to prevent duplication.")
        conn.close()
        return
    
    df = pd.read_csv(csv_path)
    df.to_sql("transactions", conn, if_exists="append", index=False)
    conn.close()
    
def reset_database():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS transactions")
    conn.commit()
    conn.close()

    # Recreate empty table
    create_table()
    
def export_db_to_csv(file_path="data/exported_expenses.csv"):
    import pandas as pd
    conn = create_connection()
    df = pd.read_sql_query("SELECT * FROM transactions", conn)
    conn.close()

    if not df.empty:
        df.to_csv(file_path, index=False)
        return file_path
    return None