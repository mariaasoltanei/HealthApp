FROM python:3.10
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
RUN pip install --upgrade pip
RUN pip install -r requirements.txt || true
RUN pip install git+https://github.com/OpenMined/TenSEAL.git#egg=tenseal


# RUN git clone https://github.com/OpenMined/TenSEAL.git /tmp/TenSEAL \
#     && cd /tmp/TenSEAL \
#     && git submodule init \
#     && git submodule update \
#     && pip install .

COPY . .
EXPOSE 5000
CMD ["python", "app.py"]

