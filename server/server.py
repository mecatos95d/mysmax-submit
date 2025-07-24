from datetime import datetime
from flask import Flask, request, jsonify
from pymongo import MongoClient
from sklearn.ensemble import IsolationForest
import joblib
import numpy as np
import random
import requests
import time

app = Flask(__name__)

DB_HOST = "localhost" # "mongo"
DB_PORT = 27018 # 27017
DB_NAME = "joidb"
DB_USER = "user"
DB_PASSWORD = "password"

client = MongoClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/joidb?authSource=admin")
db = client["joidb"]
collection = db["sensor_data"]

## Initializing model
model = None
try:
    model = joblib.load('model.joblib')
    print("모델 로드 성공")
except Exception as e:
    print("모델 로드 실패:", e)
    ## Create new model if loading fails
    gen_values = [round(random.expovariate(0.1)) for _ in range(1000)]
    train_values = [v for v in gen_values if v <= 20]
    X_train = np.array(train_values).reshape(-1, 1)
    model = IsolationForest(contamination=0.2)
    model.fit(X_train)
    joblib.dump(model, 'model.joblib')

@app.route("/api/store", methods=["POST"])
def store_sensor_data():
    data = request.get_json()
    try:
        sensor_id = data["sensor_id"]
        value = data["value"]
        timestamp = data.get("timestamp", time.time())
        dt = datetime.fromtimestamp(timestamp)

        alert = None

        if model:
            value_reshaped = np.array([[value]])
            pred = model.predict(value_reshaped)
            if pred[0] == -1:
                print(f"이상치 감지: Sensor {sensor_id} = {value} at {dt}")
                alert = True

        document = {
            "sensor_id": sensor_id,
            "value": value,
            "timestamp": dt,
            "alert": alert
        }

        collection.insert_one(document)
        print(f"[Stored] Sensor {sensor_id} = {value} at {dt}")

        notification = {
            "sensor_id": sensor_id,
            "value": value,
            "timestamp": dt.isoformat(),
            "alert": alert
        }

        try:
            response = requests.post("http://localhost:6000/api/notification", json=notification) # Adjust localhost to sensor at docker?
            print("알림 전송 결과:", response.status_code)
        except Exception as e:
            print("알림 전송 실패:", e)

        return jsonify({"status": "stored"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 400

@app.route("/api/data", methods=["GET"])
def get_sensor_data():
    try:
        sensor_id = request.args.get("sensor_id", type=int)
        start_str = request.args.get("start")
        end_str = request.args.get("end")

        if sensor_id is None:
            return jsonify({"error": "sensor_id parameter is required"}), 400

        def parse_time(t_str):
            if t_str is None:
                return None
            try:
                return datetime.fromtimestamp(float(t_str))
            except:
                try:
                    return datetime.fromisoformat(t_str)
                except:
                    return None

        start_dt = parse_time(start_str)
        end_dt = parse_time(end_str)

        query = {"sensor_id": sensor_id}
        time_filter = {}
        if start_dt:
            time_filter["$gte"] = start_dt
        if end_dt:
            time_filter["$lte"] = end_dt
        if time_filter:
            query["timestamp"] = time_filter

        cursor = collection.find(query).sort("timestamp", 1)

        result = []
        for doc in cursor:
            result.append({
                "sensor_id": doc.get("sensor_id"),
                "value": doc.get("value"),
                "timestamp": doc.get("timestamp").isoformat()
            })

        return jsonify(result), 200

    except Exception as e:
        print("Error in get_sensor_data:", e)
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)