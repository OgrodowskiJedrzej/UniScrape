FROM python:3.12-slim

WORKDIR /uniscrape

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    poppler-utils \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

COPY uniscrape/ .

CMD ["python", "core.py"]
