# HRMS Lite

A lightweight Human Resource Management System built with FastAPI (backend) and React (frontend).

![HRMS Lite](https://img.shields.io/badge/HRMS-Lite-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-61DAFB?logo=react)

## 🚀 Live Demo

- **Frontend**: [https://hrms-lite.vercel.app](https://hrms-lite.vercel.app) *(update after deployment)*
- **Backend API**: [https://hrms-lite-api.onrender.com](https://hrms-lite-api.onrender.com) *(update after deployment)*

## 📋 Features

- **Employee Management**: Add, view, and delete employees
- **Attendance Tracking**: Mark daily attendance (Present/Absent)
- **Dashboard**: Quick overview with statistics
- **RESTful API**: Complete CRUD operations

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend** | React + Vite |
| **Backend** | FastAPI (Python) |
| **Database** | SQLite |
| **Deployment** | Vercel (Frontend), Render (Backend) |

## 🏃 Run Locally

### Prerequisites
- Python 3.9+
- Node.js 18+

### 1. Clone Repository

```bash
git clone https://github.com/Raghav-2801/HRMS.git
cd HRMS
```

### 2. Start Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate (Mac/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn main:app --reload --port 8000
```

Backend will run at: `http://127.0.0.1:8000`

API Docs: `http://127.0.0.1:8000/docs`

### 3. Start Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend will run at: `http://localhost:5173`

---

## 📦 Deployment Guide

### Step 1: Push to GitHub

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - HRMS Lite"

# Add remote (replace with your repo URL)
git remote add origin https://github.com/Raghav-2801/HRMS.git

# Push
git push -u origin main
```

---

### Step 2: Deploy Backend to Render

1. Go to [render.com](https://render.com) and sign up/login
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure:

| Setting | Value |
|---------|-------|
| **Name** | hrms-lite-api |
| **Root Directory** | `backend` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Plan** | Free |

5. Click **Create Web Service**
6. Wait for deployment to complete
7. Copy your backend URL (e.g., `https://hrms-lite-api.onrender.com`)

---

### Step 3: Deploy Frontend to Vercel

1. Go to [vercel.com](https://vercel.com) and sign up/login
2. Click **"Add New..."** → **"Project"**
3. Import your GitHub repository
4. Configure:

| Setting | Value |
|---------|-------|
| **Framework Preset** | Vite |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |

5. Add Environment Variable:
   - **Name**: `VITE_API_URL`
   - **Value**: `https://hrms-lite-api.onrender.com/api` *(your Render URL + /api)*

6. Click **Deploy**
7. Wait for deployment to complete

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/dashboard/stats` | Get dashboard statistics |
| `POST` | `/api/employees` | Create employee |
| `GET` | `/api/employees` | List all employees |
| `GET` | `/api/employees/{id}` | Get employee details |
| `DELETE` | `/api/employees/{id}` | Delete employee |
| `POST` | `/api/attendance` | Mark attendance |
| `GET` | `/api/attendance` | List all attendance |
| `GET` | `/api/attendance/{employee_id}` | Get employee attendance |

---

## 📁 Project Structure

```
HRMS/
├── backend/               # FastAPI Backend
│   ├── main.py           # Main application
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── database.py       # DB connection
│   └── requirements.txt  # Python dependencies
│
├── frontend/              # React Frontend
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── api.js       # API client
│   │   ├── App.jsx      # Main app
│   │   └── styles.css   # Styles
│   ├── package.json
│   └── vite.config.js
│
└── README.md             # This file
```

---

## ⚠️ Assumptions & Limitations

- Single admin user (no authentication)
- SQLite database (data resets on Render free tier sleep)
- No payroll or leave management
- CORS enabled for all origins (restrict in production)

---

## 📝 License

MIT License - Feel free to use and modify!

---

**Built with ❤️ by Raghav**
