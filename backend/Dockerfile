FROM python:3.13-slim

RUN apt-get update && \
    apt-get install -y \
    libpq-dev \
    python3-dev \
    gcc

WORKDIR /vinyl/backend

COPY requirements.txt /vinyl/backend/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /vinyl/backend

CMD ["uvicorn", "app.main:create_app", "--host", "0.0.0.0", "--port", "8000"]
