FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir websockets

COPY sensor.py .

CMD ["python", "sensor.py"]