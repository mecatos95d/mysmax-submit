from datetime import datetime, timedelta
from pymongo import MongoClient
from sklearn.ensemble import IsolationForest
import joblib
import numpy as np
import random

DB_HOST = "localhost" # "mongo"
DB_PORT = 27018 # 27017
DB_NAME = "joidb"
DB_USER = "user"
DB_PASSWORD = "password"

client = MongoClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin")
db = client[DB_NAME]
collection = db["sensor_data"]

def train_model_from_db():
    now = datetime.now()
    day_ago = now - timedelta(hours=24)

    print(now, day_ago)

    query = {
        "timestamp": {"$gte": day_ago, "$lte": now},
        "alert": {"$ne": True}
    }

    print(query)

    print(collection)

    cursor = collection.find(query, {"value": 1, "_id": 0})
    values = [doc["value"] for doc in cursor if "value" in doc]

    if not values:
        print("학습할 정상 데이터가 없습니다.")
        return None

    X_train = np.array(values).reshape(-1, 1)

    model = None
    try:
        model = joblib.load('model.joblib')
    except Exception as e:
        ## Create new model if loading fails
        gen_values = [round(random.expovariate(0.1)) for _ in range(1000)]
        train_values = [v for v in gen_values if v <= 20]
        X_train = np.array(train_values).reshape(-1, 1)
        model = IsolationForest(contamination=0.2)
        model.fit(X_train)
        joblib.dump(model, 'model.joblib')
    model.fit(X_train)

    joblib.dump(model, 'model.joblib')
    print(f"학습 완료: 정상 데이터 {len(values)}건으로 모델 저장")

    return model

if __name__ == "__main__":
    train_model_from_db()
