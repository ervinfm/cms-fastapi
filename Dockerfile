# Gunakan base image Python
FROM python:3.11

# Set working directory di dalam container
WORKDIR /app

# Copy file requirements dan instal dependensi
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file proyek ke dalam container
COPY . .

# Expose port aplikasi (default FastAPI: 8000)
EXPOSE 8000

# Perintah untuk menjalankan aplikasi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

