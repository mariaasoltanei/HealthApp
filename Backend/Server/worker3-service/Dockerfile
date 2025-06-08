FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    cmake \
    g++ \
    python3-dev \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY model.pkl .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt || true
RUN pip install git+https://github.com/OpenMined/TenSEAL.git#egg=tenseal 
COPY . .

EXPOSE 6000

CMD ["python", "app.py"]
