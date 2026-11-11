# 1. 가벼운 파이썬 인텔/ARM 공용 베이스 이미지 사용
FROM python:3.11-slim

# 2. 작업 디렉토리 설정
WORKDIR /app

# 3. 패키지 목록을 복사하고 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 소스 코드 전체 복사
COPY . .

# 5. Flask 기본 포트 개방
EXPOSE 5000

# 6. 애플리케이션 실행
CMD ["python", "app.py"]