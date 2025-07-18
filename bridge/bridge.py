import asyncio
import json
import requests
import websockets

WS_URL = "ws://localhost:6789" # "ws://sensor:6789"
API_URL = "http://localhost:5000/api/store" # "http://server:5000/api/store"

async def bridge():
    while True:
        try:
            async with websockets.connect(WS_URL) as websocket:
                print("브릿지: WebSocket 연결됨")
                while True:
                    msg = await websocket.recv()
                    try:
                        data_list = json.loads(msg)
                        print(f"브릿지: 수신된 데이터: {data_list}")
                        for data in data_list:
                            response = requests.post(API_URL, json=data)
                            print(f"POST 결과: {response.status_code}, {response.text}")
                    except Exception as e:
                        print("브릿지 에러:", e)
        except Exception as e:
            print("WebSocket 연결 에러, 5초 후 재시도:", e)
            await asyncio.sleep(5)

if __name__ == "__main__":
    asyncio.run(bridge())
