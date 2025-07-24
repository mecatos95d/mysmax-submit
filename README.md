# JOI Task

## 실행

### 실행 전

도커 실행 및 pip 라이브러리 설치

```
docker-compose up -d
./init.sh
```

### 실행

```
./exec.sh
```

### 주기적 학습 실행

```
python train/train.py
```

#### 학습에 사용할 데이터 DB에 추가 (docker로 mongo가 돌아갈 때)

```
python train/add_data.py
```

### 실행 후 종료

```
docker-compose down
```

## API 테스팅

### /api/data

Examples

```
curl "http://localhost:5000/api/data?sensor_id=1&start=1721300000&end=1721400000"
curl "http://localhost:5000/api/data?sensor_id=1&start=2025-07-17T00:00:00&end=2025-07-18T00:00:00"
```

## 주기적 학습 스케쥴링 예제

Cron : [cron.txt](cron.txt)

Windows 스케쥴러 : [schedule.bat](schedule.bat)

## 기타 문서

### 아키텍쳐

https://docs.google.com/presentation/d/1M4x-qwBNo3hI0BVvQ7tV7cSKAoXlmqKXwC2es4Usiyc/edit?usp=sharing
