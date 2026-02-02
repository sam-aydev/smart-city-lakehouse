## We are going to simulate the IoT sensors by using randoms method in python
import time
import json 
import random
import os
from datetime import datetime

OUTPUT_PATH="/Volumes/smart_city_prod/transportation/raw"


def generate_iot_data():
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    sensors = ["SN-101", "SN-102", "SN-103", "SN-104", "SN-105"]
    print(sensors)
    try:
        while True:

            sensor_id = random.choice(sensors)
            is_anomaly = random.random() > 0.95
            print(sensor_id, is_anomaly)
            if is_anomaly:
                temp = round(random.uniform(90, 120), 2)
                vibration = round(random.uniform(0, 5), 2)
                status = "critical"
            else:
                temp = round(random.uniform(20, 80), 2)
                vibration = round(random.uniform(0, 1), 2)
                status = "nominal"
            print(temp, vibration, status)
            data = {
                "sensor_id": sensor_id,
                "timestamp": datetime.now().isoformat(),
                "temp_celsius": temp,
                "vibration_g": vibration,
                "status": status,
                "software_version": "v2.1"
            }


            file_name = f"{sensor_id}_{int(time.time()* 1000)}.json"
            file_path = os.path.join(OUTPUT_PATH, file_name)

            with open(file_path, "w") as f:
                json.dump(data, f)
                print(f"Generated data for {sensor_id} and wrote to {file_path} with a status {status}")
                time.sleep(3)
    except KeyboardInterrupt:
        print("\n Simulation stopped")

print(generate_iot_data())




