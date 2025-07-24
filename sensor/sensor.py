
from flask import Flask, request, jsonify
import asyncio
import json
import random
import time
import threading
import websockets

app = Flask(__name__)

@app.route("/api/notification", methods=["POST"])
def handle_notification():
    data = request.get_json()
    print("[센서에서 알림 수신]", data)
    return jsonify({"status": "received"}), 200

def run_flask():
    app.run(host="0.0.0.0", port=6000)

address = "0.0.0.0"
port = 6789

async def send_sensor_data(websocket):
    while True:
        try:
            data_list = []
            for i in range(5):
                value = round(random.expovariate(0.1))
                data = {
                    "sensor_id": i+1,
                    "value": value,
                    "timestamp": time.time()
                }
                data_list.append(data)
            await websocket.send(json.dumps(data_list))
            await asyncio.sleep(1)
        except Exception as e:
            print("WebSocket send error:", e)
            break

async def websocket_main():
    async with websockets.serve(send_sensor_data, address, port):
        print(f"WebSocket 서버 실행 중 (ws://{address}:{port})")
        await asyncio.Future()  # 무한 대기

def run_websocket():
    asyncio.run(websocket_main())

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    run_websocket()
