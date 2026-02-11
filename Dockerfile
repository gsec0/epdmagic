FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install build + runtime deps for Pillow
RUN apt-get update && apt-get install -y \
    python3-dev \
    libjpeg-dev \
    libtiff-dev \
    libpng-dev \
    libfreetype6-dev \
    libwebp-dev \
    libopenjp2-7-dev \
    libx11-dev \
    libxext-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
