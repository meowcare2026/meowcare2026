# 🐱 MeowCare Backend API

REST API untuk aplikasi **MeowCare – Sistem Pakar Diagnosis Penyakit Kucing** menggunakan **FastAPI**, **Supabase PostgreSQL**, dan **Supabase Authentication**.

Backend ini dikembangkan menggunakan arsitektur **Layered Architecture (Controller → Service → Repository)** sehingga mudah dikembangkan, diuji, dan dipelihara.

---

# Tech Stack

- Python 3.12+
- FastAPI
- Uvicorn
- Supabase PostgreSQL
- Supabase Auth
- Pydantic v2
- HTTPX
- JWT Authentication
- Swagger / OpenAPI

---

# Project Structure

```
meowcare-backend/
│
├── app/
│
├── config/
│   ├── settings.py
│   ├── database.py
│   ├── supabase.py
│   └── security.py
│
├── controllers/
├── middleware/
├── repositories/
├── routers/
├── schemas/
├── services/
├── utils/
│
├── tests/
│
├── .env
├── .env.example
├── requirements.txt
├── README.md
└── run.py
```

---

# Installation

Clone project

```bash
git clone https://github.com/meowcare2026/meowcare2026.git
```

Masuk ke project

```bash
cd meowcare-backend
```

Buat Virtual Environment

```bash
python -m venv .venv
```

Windows

```bash
.venv\Scripts\activate
```

Linux / Mac

```bash
source .venv/bin/activate
```

Install dependency

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Copy file

```bash
cp .env.example .env
```

Isi konfigurasi berikut

```env
APP_NAME=MeowCare API
APP_VERSION=1.0.0
APP_ENV=development
DEBUG=True

API_V1_PREFIX=/api/v1

SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

JWT_SECRET_KEY=
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

---

# Run Application

```bash
uvicorn app.main:app --reload
```

API

```
http://127.0.0.1:8000
```

Swagger

```
http://127.0.0.1:8000/docs
```

Redoc

```
http://127.0.0.1:8000/redoc
```

---

# Authentication

Sistem menggunakan

- Supabase Authentication
- JWT Bearer Token

Flow

```
Register
      ↓
Login
      ↓
Access Token
      ↓
Bearer Token
      ↓
Protected Endpoint
```

Contoh Header

```
Authorization: Bearer ACCESS_TOKEN
```

---

# API Endpoints

## Authentication

| Method | Endpoint |
|---------|----------|
| POST | /admin/auth/register |
| POST | /admin/auth/login |
| GET | /admin/auth/me |
| POST | /admin/auth/logout |

---

## Dashboard

| Method | Endpoint |
|---------|----------|
| GET | /admin/dashboard |

---

## Diseases

| Method | Endpoint |
|---------|----------|
| GET | /admin/diseases |
| POST | /admin/diseases |
| GET | /admin/diseases/{id} |
| PUT | /admin/diseases/{id} |
| DELETE | /admin/diseases/{id} |

---

## Symptoms

| Method | Endpoint |
|---------|----------|
| GET | /admin/symptoms |
| POST | /admin/symptoms |
| GET | /admin/symptoms/{id} |
| PUT | /admin/symptoms/{id} |
| DELETE | /admin/symptoms/{id} |

---

## Rules

| Method | Endpoint |
|---------|----------|
| GET | /admin/rules |
| POST | /admin/rules |
| GET | /admin/rules/{id} |
| PUT | /admin/rules/{id} |
| DELETE | /admin/rules/{id} |

---

## Admin Logs

| Method | Endpoint |
|---------|----------|
| GET | /admin/logs |
| GET | /admin/logs/{id} |

---

# Database

Tabel utama

- admin_profiles
- admin_logs
- diseases
- symptoms
- rules

Relasi

```
Admin
   │
   └──────────────┐
                  │
                  ▼
            Admin Logs

Disease
      │
      ├─────────────┐
      │             │
      ▼             ▼
    Rules        Diagnosis (Backend 2)

Symptom
      │
      ├─────────────┐
      │             │
      ▼             ▼
    Rules        Diagnosis (Backend 2)
```

---

# Response Format

Success

```json
{
    "success": true,
    "message": "Success",
    "data": {},
    "meta": null
}
```

Error

```json
{
    "success": false,
    "message": "Validation Error",
    "error": {
        "code": "VALIDATION_ERROR",
        "details": {}
    }
}
```

---

# Role Permission

| Role | Permission |
|------|------------|
| superadmin | Full Access |
| pakar | CRUD Rules |
| admin | CRUD Diseases & Symptoms |

---

# Logging

Setiap aktivitas admin akan disimpan pada tabel

```
admin_logs
```

Contoh aktivitas

- Login
- Logout
- Create Disease
- Update Disease
- Delete Disease
- Create Symptom
- Update Symptom
- Delete Symptom
- Create Rule
- Update Rule
- Delete Rule

---

# Validation

Sistem melakukan validasi

- Required Field
- UUID
- Duplicate Code
- Duplicate Name
- CF Expert 0-1
- Authorization
- Role Permission
- Foreign Key

---

# HTTP Status Code

| Code | Description |
|------|-------------|
|200|OK|
|201|Created|
|400|Bad Request|
|401|Unauthorized|
|403|Forbidden|
|404|Not Found|
|409|Conflict|
|422|Validation Error|
|500|Internal Server Error|

---

# Backend Developer Scope

## Backend Developer 1

- Authentication Admin
- Dashboard
- CRUD Diseases
- CRUD Symptoms
- CRUD Rules
- Admin Logs
- Middleware
- JWT Authentication
- Swagger
- Database Integration

---

## Backend Developer 2

- Diagnosis
- Certainty Factor Engine
- Diagnosis History
- Diagnosis Result
- PDF Report
- Public API
- User Diagnosis

---

# Testing

Jalankan aplikasi

```bash
uvicorn app.main:app --reload
```

Buka Swagger

```
http://127.0.0.1:8000/docs
```

Atau gunakan Postman.

---

# License

MeowCare Backend

Copyright © 2026

Developed for MeowCare Expert System Project.
