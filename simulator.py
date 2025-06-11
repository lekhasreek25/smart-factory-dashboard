import requests
import random
import time

while True:
    data = {
        "temperature": round(random.uniform(20, 45), 2),
        "humidity": round(random.uniform(30, 80), 2)
    }

    try:
        response = requests.post("http://127.0.0.1:5000/data", json=data)
        print(f"Sent: {data} | Status: {response.status_code}")
    except Exception as e:
        print("❌ Failed to send:", e)

    time.sleep(5)
