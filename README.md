# 💰 Expense Tracker Pro (IoT Enabled)

A Real-Time IoT-Integrated Expense Tracking System using **ESP32 + WiFi + Flask API + Streamlit + SQLite**

---

## 📌 Project Overview

Expense Tracker Pro is an IoT-enabled financial analytics dashboard that allows real-time expense logging using an **ESP32 Dev Board** connected over WiFi.

The system enables:

* Real-time expense logging via physical buttons
* WiFi-based HTTP communication
* Automatic database storage
* Interactive dashboard visualization
* Full CRUD operations
* CSV import/export support

This project demonstrates integration of:

* Embedded Systems (ESP32)
* REST API Architecture
* Database Management
* Data Analytics Dashboard

The system uses:

* **Streamlit** (Frontend Dashboard)
* **SQLite** (Database Storage)
* **Pandas** (Data Processing)
* **Matplotlib / Streamlit Charts** (Visualization)
* **Arduino IDE** (ESP32 Development)

---

# 🏗 Project Architecture

```
Expense_Tracker_App_Project/
│
├── data/
│   ├── expenses.csv
│   ├── cleaned_expenses.csv
│
├── ESP32_Code/
│   ├── expense_logger.ino   
│
├── src/
│   ├── database.py
│   ├── preprocessing.py
│   ├── api_server.py
│
├── expenses.db
├── app.py
├── simulate_esp32.py (for simulation purpose if someone doesn't possess any real hardware)
├── requirements.txt
└── README.md
```

---

# 🔌 System Architecture (IoT Flow)

```
ESP32 Dev Board (WiFi + NTP Time)
        ↓
HTTP POST Request
        ↓
Flask API Server (Python)
        ↓
SQLite Database (expenses.db)
        ↓
Streamlit Dashboard (Real-Time View)
```

---

# ⚙️ Tech Stack

### 💻 Software

* Python 3.x
* Streamlit
* Flask
* SQLite
* Pandas
* Matplotlib

### 🔌 Hardware

* ESP32 Dev Board
* Push Buttons
* WiFi Network
* Arduino IDE

---

# 📦 Features

## ✅ IoT-Based Real-Time Logging

* Physical button press logs transaction
* Device sends date & month via NTP
* HTTP API stores data in SQLite

## ✅ Dashboard Features

* Live auto-refresh
* Add manual transactions
* Edit raw data
* Multi-row deletion
* Export database to CSV
* Reset database

## ✅ Data Loading Modes

* Default Mode (preloaded dataset)
* Manual Mode (custom CSV upload)

## ✅ CRUD Support

* Create
* Read
* Update
* Delete

---

# 🧹 Data Preprocessing Flow

When CSV is loaded:

1. Columns normalized to lowercase
2. Date converted to datetime
3. Data inserted into SQLite
4. Dashboard dynamically calculates month
5. Charts update automatically

---

# 🚀 Installation Guide

## 1️⃣ Clone or Extract Project

Extract to:

```
C:\Users\YourName\Desktop\Expense_Tracker_App_Project
```

---

## 2️⃣ Install Python Dependencies

```bash
pip install -r requirements.txt
```

If needed:

```bash
python -m pip install -r requirements.txt
```

---

# 🔌 ESP32 Setup (Arduino IDE)

## 1️⃣ Install ESP32 Board in Arduino IDE

1. Open Arduino IDE
2. Go to **File → Preferences**
3. Add this URL in Additional Boards Manager:

```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```

4. Go to **Tools → Board → Boards Manager**
5. Install **ESP32 by Espressif Systems**
6. Select **ESP32 Dev Module**

---

## 2️⃣ Upload ESP32 Code

Open Arduino IDE and paste the ESP32 WiFi + HTTP code provided in the project.

Important:

Update these values:

```cpp
const char* ssid = "YOUR_WIFI_NAME";
const char* password = "YOUR_WIFI_PASSWORD";
const char* serverURL = "http://YOUR_PC_IP:5000/add";
```

Find your PC IPv4 using:

```bash
ipconfig
```

Example:

```
192.168.1.1
```

Then use:

```cpp
http://192.168.1.1:5000/add
```

Upload the code to ESP32.

---

# ▶ Running the Full IoT System

## Step 1 — Start API Server

Open terminal:

```bash
python src/api_server.py
```

You should see:

```
Running on http://0.0.0.0:5000
```

---

## Step 2 — Start Streamlit Dashboard

In new terminal:

```bash
python -m streamlit run app.py
```

Open:

```
http://localhost:8501
```

---

## Step 3 — Press ESP32 Button

* Button press sends HTTP request
* API stores data
* Streamlit auto-refresh updates dashboard

---

# 📊 How to Use Dashboard

## 🔹 Add Manual Transaction

* Fill form
* Click Add
* Data saved instantly

## 🔹 Edit Transactions

* Enable Editable Table
* Modify cell
* Save changes

## 🔹 Delete Multiple Rows

* Select rows
* Click Delete Selected

## 🔹 Export Database

* Click Export DB to CSV
* Download formatted file

## 🔹 Reset Database

* Clears all records
* Recreates table

---

# 🗄 Database Details

File:

```
expenses.db
```

Table:

```
transactions
```

Schema:

| Column      | Type                |
| ----------- | ------------------- |
| id          | INTEGER PRIMARY KEY |
| date        | TEXT                |
| category    | TEXT                |
| description | TEXT                |
| amount      | REAL                |
| type        | TEXT                |

Month is dynamically calculated in Streamlit using date.

---

# 🧠 Important Notes

* ESP32 and PC must be on same WiFi
* Windows Firewall must allow port 5000
* API must be running before pressing button
* Date is obtained using NTP server
* Dashboard auto-refreshes every 2 seconds

---

# 🔒 Best Practices Implemented

* RESTful API design
* Parameterized SQL queries
* Absolute database paths
* Real-time IoT integration
* Separation of concerns (API vs UI)
* Clean UI state management

---

# 📈 Future Enhancements

* Multi-device analytics
* Device ID tracking
* Budget alerts
* PostgreSQL migration
* Cloud deployment (Render / Railway)
* HTTPS security
* JWT authentication
* MQTT-based IoT upgrade

---

# 🧪 Tested On

* Python 3.10+
* Streamlit 1.30+
* ESP32 Dev Module
* Windows 10 / 11

---

# 🎯 Final Outcome

This project demonstrates:

* IoT hardware integration
* Real-time REST API communication
* Database-backed analytics
* Financial dashboard visualization
* Production-style system architecture

This is a portfolio-grade IoT + Data Engineering project.

---

## 👤 Author

**Kusan Chakraborty**
B.Tech – Computer Science & Engineering (Data Science)

---

## 📄 License

This project is licensed under the **MIT License**.

You are free to:

* Use
* Modify
* Distribute

This software, provided proper credit is given to the author.

© 2026 Kusan Chakraborty
