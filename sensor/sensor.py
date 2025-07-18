import asyncio
import websockets
import json
import random
import time

address = "localhost" # "0.0.0.0"

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

async def main():
    print("WebSocket 서버 실행 준비 중...")
    async with websockets.serve(send_sensor_data, address, 6789):
        print(f"WebSocket 서버 실행 중 (ws://{address}:6789)")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
