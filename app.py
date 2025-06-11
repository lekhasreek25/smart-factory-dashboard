# ✅ app.py
from flask import Flask, render_template, request, redirect, send_file
from datetime import datetime
import sqlite3
import csv
import os

app = Flask(__name__)
email_alerts_enabled = True

# ✅ Store to SQLite
def insert_data(timestamp, temp, hum):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO readings (timestamp, temperature, humidity) VALUES (?, ?, ?)", (timestamp, temp, hum))
    conn.commit()
    conn.close()

# ✅ Read from SQLite (latest 20 entries)
def get_data():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 20")
    rows = cursor.fetchall()
    conn.close()
    return rows[::-1]  # reverse for chronological order

@app.route('/')
def index():
    data = get_data()
    return render_template("index.html", data=data, email_alerts_enabled=email_alerts_enabled)

@app.route('/data', methods=['POST'])
def receive_data():
    json_data = request.get_json()
    temp = float(json_data['temperature'])
    hum = float(json_data['humidity'])
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    insert_data(now, temp, hum)

    if email_alerts_enabled and temp > 40:
        send_email_alert(temp, hum)

    return 'OK'

@app.route('/toggle_email', methods=['POST'])
def toggle_email():
    global email_alerts_enabled
    email_alerts_enabled = 'email_alerts' in request.form
    return redirect('/')

@app.route('/export')
def export_csv():
    filename = 'sensor_export.csv'
    data = get_data()
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Time', 'Temperature', 'Humidity'])
        for row in data:
            writer.writerow([row['timestamp'], row['temperature'], row['humidity']])
    return send_file(filename, as_attachment=True)

def send_email_alert(temp, hum):
    print(f"EMAIL ALERT 🚨: Temperature = {temp} °C, Humidity = {hum} %")

if __name__ == '__main__':
    app.run(debug=False)
