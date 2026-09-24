FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY miniapp/requirements.txt ./miniapp/requirements.txt

RUN pip install --no-cache-dir -r miniapp/requirements.txt

COPY app ./app
COPY miniapp ./miniapp

CMD ["sh", "-c", "uvicorn miniapp.main:app --host 0.0.0.0 --port ${PORT:-8000}"]