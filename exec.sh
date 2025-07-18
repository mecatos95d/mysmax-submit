docker-compose down
docker-compose up -d
pip install --no-cache-dir websockets requests FLASK pymongo tsai
python server/server.py &
python sensor/sensor.py &
python bridge/bridge.py &