from flask import Flask, render_template, jsonify
import datetime
import random

app = Flask(__name__)

# ---------------- CONFIG ----------------
TARIFF_PER_KWH = 6.0     # ₹6 per unit (realistic Indian tariff)
UPDATE_INTERVAL_SEC = 2 # frontend refresh rate

history = []

# ---------------- HELPERS ----------------
def get_house_power():
    # Simulated whole-house power (W)
    return round(random.uniform(500, 3000), 2)

def predict_next(power):
    return round(power + random.uniform(-150, 150), 2)

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/data")
def data():
    total_power = get_house_power()
    predicted = predict_next(total_power)

    # Energy for this 2-second interval (kWh)
    energy_kwh = (total_power * UPDATE_INTERVAL_SEC) / (1000 * 3600)

    # Cost for this interval
    cost = round(energy_kwh * TARIFF_PER_KWH, 4)

    record = {
        "time": datetime.datetime.now().strftime("%H:%M:%S"),
        "total": total_power,
        "predicted": predicted,
        "energy": round(energy_kwh, 6),
        "cost": cost
    }

    history.append(record)
    if len(history) > 1000:
        history.pop(0)

    # -------- ANALYTICS --------
    daily_energy = round(sum(r["energy"] for r in history), 4)  # kWh
    daily_cost = round(sum(r["cost"] for r in history), 2)
    monthly_cost = round(daily_cost * 30, 2)

    return jsonify({
        "current": record,
        "history": history[-10:],
        "analytics": {
            "daily_energy": daily_energy,
            "daily_cost": daily_cost,
            "monthly_cost": monthly_cost
        }
    })

if __name__ == "__main__":
    app.run(debug=True)              