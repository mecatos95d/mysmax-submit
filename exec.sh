trap "echo '종료 중...'; pkill -P $$; exit" SIGINT
python server/server.py &
python sensor/sensor.py &
python bridge/bridge.py &
wait