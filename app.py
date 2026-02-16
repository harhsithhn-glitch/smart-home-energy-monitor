from flask import Flask, render_template, jsonify, send_file
import datetime
import random
import sqlite3
import csv
import os

app = Flask(__name__)

# ---------------- CONFIG ----------------
TARIFF_PER_KWH = 6.0
UPDATE_INTERVAL_SEC = 2
DB_NAME = "energy.db"

# ---------------- DATABASE ----------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS energy_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            total_power REAL,
            energy REAL,
            cost REAL,
            fan REAL,
            ac REAL,
            tv REAL,
            fridge REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- HELPERS ----------------
def simulate_devices():
    fan = random.uniform(60, 100)
    ac = random.uniform(800, 1500)
    tv = random.uniform(80, 200)
    fridge = random.uniform(150, 300)
    return fan, ac, tv, fridge

def moving_average_prediction():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT total_power FROM energy_data ORDER BY id DESC LIMIT 5")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return 0

    avg = sum(r[0] for r in rows) / len(rows)
    return round(avg + random.uniform(-50, 50), 2)

def insert_record(data):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO energy_data 
        (timestamp, total_power, energy, cost, fan, ac, tv, fridge)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, data)
    conn.commit()
    conn.close()

def get_daily_stats():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    today = datetime.date.today().strftime("%Y-%m-%d")

    c.execute("""
        SELECT SUM(energy), SUM(cost)
        FROM energy_data
        WHERE DATE(timestamp) = ?
    """, (today,))

    result = c.fetchone()
    conn.close()

    daily_energy = round(result[0] or 0, 4)
    daily_cost = round(result[1] or 0, 2)
    monthly_cost = round(daily_cost * 30, 2)

    return daily_energy, daily_cost, monthly_cost

def get_recent_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT timestamp, total_power, energy, cost
        FROM energy_data
        ORDER BY id DESC
        LIMIT 10
    """)
    rows = c.fetchall()
    conn.close()

    history = []
    for r in rows:
        history.append({
            "time": r[0],
            "total": r[1],
            "energy": round(r[2], 6),
            "cost": r[3]
        })

    return list(reversed(history))

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    fan, ac, tv, fridge = simulate_devices()
    total_power = round(fan + ac + tv + fridge, 2)

    predicted = moving_average_prediction()

    energy_kwh = (total_power * UPDATE_INTERVAL_SEC) / (1000 * 3600)
    cost = round(energy_kwh * TARIFF_PER_KWH, 4)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    insert_record((timestamp, total_power, energy_kwh, cost, fan, ac, tv, fridge))

    daily_energy, daily_cost, monthly_cost = get_daily_stats()

    return jsonify({
        "current": {
            "time": timestamp,
            "total": total_power,
            "predicted": predicted,
            "energy": round(energy_kwh, 6),
            "cost": cost,
            "fan": round(fan,2),
            "ac": round(ac,2),
            "tv": round(tv,2),
            "fridge": round(fridge,2)
        },
        "analytics": {
            "daily_energy": daily_energy,
            "daily_cost": daily_cost,
            "monthly_cost": monthly_cost
        },
        "history": get_recent_history()
    })

@app.route("/export")
def export_csv():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM energy_data")
    rows = c.fetchall()
    conn.close()

    filename = "energy_report.csv"

    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID","Timestamp","Total Power","Energy","Cost","Fan","AC","TV","Fridge"])
        writer.writerows(rows)

    return send_file(filename, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)