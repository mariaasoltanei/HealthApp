FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
COPY rf_model.pkl .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

EXPOSE 6000

CMD ["python", "app.py"]
