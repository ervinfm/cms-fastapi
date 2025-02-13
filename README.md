# Backend API Content Management dengan FastAPI, PostgreSQL, dan JWT

## 🚀 Deskripsi
Proyek ini adalah backend REST API Content Management yang menyediakan fitur autentikasi JWT, manajemen user, dan manajemen konten menggunakan FastAPI, PostgreSQL, dan SQLAlchemy.

## 🛠 Teknologi yang Digunakan
- FastAPI (Python)
- PostgreSQL
- SQLAlchemy & Alembic
- Pytest (Testing)
- JWT Authentication
- SlowAPI (Rate Limiting)
- Docker (Deployment Cepat)

---

## 🔧 Instalasi & Setup
### 1️⃣ Clone Repository
```bash
git clone https://github.com/ervinfm/cms-fastapi.git
cd cms-fastapi
```

### 2️⃣ Buat Virtual Environment & Install Dependensi
```bash
python -m venv venv
source venv/bin/activate  # Untuk Mac/Linux
venv\Scripts\activate     # Untuk Windows

pip install -r requirements.txt
```

### 3️⃣ Konfigurasi Environment Variables
Buat file `.env` dan tambahkan:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/cms
SECRET_KEY=mysecretkey12345
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
```

Ganti `username` dan `password` dengan kredensial PostgreSQL Anda.
(dalam project ini username dan password yaitu postgres)

### 4️⃣ Jalankan Database Migration
```bash
alembic upgrade head
```

### 5️⃣ Jalankan Server
```bash
uvicorn app.main:app --reload
```
API bisa diakses di:  
📌 **http://127.0.0.1:8000/docs** (Swagger UI)

---

## 📌 API Endpoints
### 🔑 **Autentikasi**
| Method | Endpoint | Deskripsi |
|--------|---------|-----------|
| POST | `/register` | Register user baru |
| POST | `/token` | Login dan dapatkan JWT |

### 👤 **Manajemen User**
| Method | Endpoint | Deskripsi |
|--------|---------|-----------|
| GET | `/users/{user_id}` | Ambil detail user |
| PUT | `/users/{user_id}` | Update user |
| DELETE | `/users/{user_id}` | Hapus user |

### 📝 **Manajemen Konten**
| Method | Endpoint | Deskripsi |
|--------|---------|-----------|
| GET | `/content/` | Ambil semua konten user |
| POST | `/content/` | Tambah konten baru |
| GET | `/content/{content_id}` | Ambil detail konten |
| PUT | `/content/{content_id}` | Update konten |
| DELETE | `/content/{content_id}` | Hapus konten |

---

## ⏳ Rate Limiting (Keamanan Tambahan)
- **Login:** Maksimal 5 request per menit
- **Register:** Maksimal 3 request per menit
- **GET User:** Maksimal 10 request per menit
- **POST Content:** Maksimal 5 request per menit
- **DELETE Content:** Maksimal 3 request per menit

---

## 📦 Deployment dengan Docker
### 1️⃣ Build Docker Image
```bash
docker build -t fastapi-app .
```
### 2️⃣ Jalankan Container
```bash
docker run -p 8000:8000 fastapi-app
```
### 3️⃣ Jalankan dengan Docker Compose
```bash
docker-compose up --build
```

---

## 🧪 Testing
Jalankan perintah berikut untuk menjalankan unit test:
```bash
pytest tests/
```

---

## 🎯 Kesimpulan Proyek
✅ **Fitur Autentikasi JWT**  
✅ **CRUD User & Content**  
✅ **Database dengan PostgreSQL & SQLAlchemy**  
✅ **Unit Test dengan Pytest**  
✅ **Rate Limiting untuk Keamanan**  
✅ **Logging & Error Handling**  
✅ **Docker untuk Deployment Cepat**  
✅ **Dokumentasi Lengkap**  

Note : Terdapat folder output yang berisikan contoh pengujian endpoint (Postman)

🔥 **Proyek siap!** 🔥

