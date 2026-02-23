FROM python:3.11-slim

WORKDIR /app

# requirements varsa önce onu kur
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# projeyi kopyala
COPY . .

# Flask 5000 kullanıyorsa
EXPOSE 5000

# app.py varsa:
CMD ["python", "app.py"]