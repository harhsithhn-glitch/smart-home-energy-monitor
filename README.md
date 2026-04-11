# ⚡ Smart Home Energy Monitor

A real-time web-based dashboard to monitor, analyze, and predict household energy consumption.
Built using **Flask, SQLite, and Chart.js**, this system provides live power tracking, cost estimation, and interactive analytics.

---

## 🚀 Features

* 🔴 **Live Power Monitoring**

  * Real-time simulation of household energy usage (Watts)

* 📊 **Interactive Charts**

  * Line chart for power trends
  * Bar chart for energy consumption

* 💰 **Cost Calculation**

  * Daily energy usage (kWh)
  * Daily electricity cost
  * Monthly bill estimation

* 📋 **Data Logging**

  * Stores all records in SQLite database
  * Tracks timestamp, power, energy, and cost

* 🎯 **Prediction System**

  * Predicts next power usage based on current trend

* 🌙 **Dark/Light Mode**

  * Toggle UI theme for better user experience

---

## 🛠️ Tech Stack

* **Backend:** Python, Flask
* **Database:** SQLite
* **Frontend:** HTML, CSS, JavaScript
* **Charts:** Chart.js

---

## 📁 Project Structure

```
smart-home-energy-monitor/
│
├── app.py
├── energy.db
│
├── templates/
│   └── index.html
│
├── static/
│   └── style.css
│
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/smart-home-energy-monitor.git
cd smart-home-energy-monitor
```

### 2. Install Dependencies

```bash
pip install flask
```

### 3. Run Application

```bash
python app.py
```

### 4. Open Browser

```
http://127.0.0.1:5000
```

---

## 📊 How It Works

* Simulates power usage every 2 seconds
* Converts power → energy (kWh)
* Calculates cost using tariff
* Stores data in database
* Displays analytics on dashboard

---

## 💡 Future Improvements

* 🔌 IoT device integration (real sensor data)
* 📱 Mobile app version
* 📈 Machine Learning for better prediction
* 🔔 Alerts for high power usage
* ☁️ Cloud deployment

---

## 📸 Screenshots

(Add your project screenshots here)

---

## 👨‍💻 Author

**Harshith H N**
IIT Bombay | Engineering Student

---

## ⭐ Contribution

Feel free to fork, improve, and contribute to this project!

---
