from flask import Flask, render_template, jsonify
import datetime
import random
import sqlite3

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
            power REAL,
            energy REAL,
            cost REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ---------------- HELPERS ----------------
def get_house_power():
    return round(random.uniform(500, 3000), 2)

def predict_next(power):
    return round(power + random.uniform(-150, 150), 2)

def insert_record(timestamp, power, energy, cost):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        INSERT INTO energy_data (timestamp, power, energy, cost)
        VALUES (?, ?, ?, ?)
    """, (timestamp, power, energy, cost))
    conn.commit()
    conn.close()

def get_recent_records(limit=10):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        SELECT timestamp, power, energy, cost
        FROM energy_data
        ORDER BY id DESC
        LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()

    records = []
    for r in rows:
        records.append({
            "time": r[0].split()[1],
            "power": r[1],
            "energy": round(r[2], 6),
            "cost": r[3]
        })
    return list(reversed(records))

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

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    total_power = get_house_power()
    predicted = predict_next(total_power)

    energy_kwh = (total_power * UPDATE_INTERVAL_SEC) / (1000 * 3600)
    cost = round(energy_kwh * TARIFF_PER_KWH, 4)

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    insert_record(timestamp, total_power, energy_kwh, cost)

    daily_energy, daily_cost, monthly_cost = get_daily_stats()
    recent_records = get_recent_records()

    return jsonify({
        "current": {
            "time": timestamp.split()[1],
            "total": total_power,
            "predicted": predicted,
            "energy": round(energy_kwh, 6),
            "cost": cost
        },
        "history": recent_records,
        "analytics": {
            "daily_energy": daily_energy,
            "daily_cost": daily_cost,
            "monthly_cost": monthly_cost
        }
    })

if __name__ == "__main__":
    app.run(debug=False)