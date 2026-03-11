# HRMS Lite — Human Resource Management System

![Backend Tests](https://github.com/kapilraghav2801/HRMS/actions/workflows/test.yml/badge.svg)

A lightweight HRMS REST API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**,  
with full CRUD for employees and attendance tracking.

---

## Features

- Employee management (create, list, search, update, delete)
- Attendance tracking with duplicate-prevention and cascade delete
- Dashboard statistics (totals, today's attendance, department breakdown)
- Pydantic v2 validation with enum-based attendance statuses
- SQLite for local dev / tests — PostgreSQL for production (Render.com)
- 43-test suite with **96 % coverage** (threshold: 70 %)
- GitHub Actions CI on every push/PR to `main`

---

## Project Structure

```
HRMS-Mar/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── enums.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── employee.py
│   │   └── attendance.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── employees.py
│   │   ├── attendance.py
│   │   └── dashboard.py
│   └── schemas/
│       ├── __init__.py
│       ├── employee.py
│       └── attendance.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_employees.py
│   ├── test_attendance.py
│   └── test_dashboard.py
├── .github/
│   └── workflows/
│       └── test.yml
├── .env.example
├── pytest.ini
├── render.yaml
└── requirements.txt
```

---

## Quick Start

```bash
# 1. Clone & install
git clone https://github.com/kapilraghav2801/HRMS.git
cd HRMS
pip install -r requirements.txt

# 2. Copy env and run
cp .env.example .env
uvicorn app.main:app --reload --port 8000
```

API docs available at [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Running Tests

```bash
pytest
```

---

## Environment Variables

| Variable            | Default                     | Description                          |
| ------------------- | --------------------------- | ------------------------------------ |
| `DATABASE_URL`      | `sqlite:///./hrms_local.db` | Production DB (PostgreSQL on Render) |
| `TEST_DATABASE_URL` | `sqlite:///./test_hrms.db`  | Test DB (SQLite in-memory)           |
| `CORS_ORIGINS`      | `http://localhost:5173,...` | Comma-separated allowed origins      |

---

## API Endpoints

See [API.md](API.md) for full documentation.

| Method         | Path                          | Description                  |
| -------------- | ----------------------------- | ---------------------------- |
| GET            | `/api/health`                 | Health check                 |
| POST           | `/api/employees/`             | Create employee              |
| GET            | `/api/employees/`             | List / search employees      |
| GET            | `/api/employees/departments`  | List departments             |
| GET            | `/api/employees/{id}`         | Get employee                 |
| PUT            | `/api/employees/{id}`         | Update employee              |
| DELETE         | `/api/employees/{id}`         | Delete employee              |
| GET            | `/api/employees/{id}/summary` | Attendance summary           |
| POST           | `/api/attendance/`            | Mark attendance              |
| GET            | `/api/attendance/`            | List attendance (filters)    |
| GET            | `/api/attendance/today`       | Today's attendance           |
| GET/PUT/DELETE | `/api/attendance/{id}`        | Get / update / delete record |
| GET            | `/api/dashboard/stats`        | Dashboard statistics         |
