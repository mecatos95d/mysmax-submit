from datetime import datetime, timedelta
from pymongo import MongoClient
import random

DB_HOST = "localhost" # "mongo"
DB_PORT = 27018 # 27017
DB_NAME = "joidb"
DB_USER = "user"
DB_PASSWORD = "password"

client = MongoClient(f"mongodb://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin")
db = client[DB_NAME]
collection = db["sensor_data"]

def save_dummy_data():
    start_time = datetime.now() - timedelta(hours=24)
    end_time = datetime.now()
    total_seconds = int((end_time - start_time).total_seconds())

    for second_offset in range(total_seconds + 1):
        timestamp = start_time + timedelta(seconds=second_offset)
        for sensor_id in range(1, 6):
            value = round(random.expovariate(0.1))
            document = {
                "sensor_id": sensor_id,
                "value": value,
                "timestamp": timestamp,
                "alert": True if value > 20 else None
            }
            collection.insert_one(document)
        if second_offset % 3600 == 0:  # 1시간마다 진행 상황 출력
            print(f"{second_offset // 3600} hours generated...")
    print(f"더미 데이터 {total_seconds * 5}건 저장 완료")

if __name__ == "__main__":
    save_dummy_data()
