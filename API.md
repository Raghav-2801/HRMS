# HRMS Lite – API Reference

Base URL (local): `http://localhost:8000`  
Interactive docs: `http://localhost:8000/docs`

---

## Health

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Health check |

**Response**
```json
{ "status": "ok", "version": "2.0.0" }
```

---

## Employees

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/employees/` | Create employee |
| GET | `/api/employees/` | List employees (search + filter) |
| GET | `/api/employees/departments` | List distinct departments |
| GET | `/api/employees/{id}` | Get employee by UUID |
| PUT | `/api/employees/{id}` | Update employee |
| DELETE | `/api/employees/{id}` | Delete employee (cascades attendance) |
| GET | `/api/employees/{id}/summary` | Get attendance summary for employee |

### POST `/api/employees/`

**Request body**
```json
{
  "employee_id": "EMP001",
  "name": "Kapil Raghav",
  "email": "kapil@example.com",
  "department": "Engineering",
  "position": "Backend Developer"
}
```

**Responses**
- `201` – Created
- `409` – Duplicate employee_id or email
- `422` – Validation error

### GET `/api/employees/`

**Query params**
| Param | Type | Description |
|-------|------|-------------|
| `search` | string | Search by name, email, or employee_id |
| `department` | string | Filter by exact department |

### PUT `/api/employees/{id}`

All fields optional:
```json
{
  "name": "New Name",
  "email": "new@example.com",
  "department": "DevOps",
  "position": "Senior Developer"
}
```

### GET `/api/employees/{id}/summary`

**Response**
```json
{
  "employee": { "...employee fields..." },
  "total_days": 20,
  "present": 15,
  "absent": 3,
  "late": 1,
  "half_day": 1,
  "attendance_rate": 85.0
}
```

---

## Attendance

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/attendance/` | Mark attendance |
| GET | `/api/attendance/today` | Today's attendance for all employees |
| GET | `/api/attendance/` | List records (filterable) |
| GET | `/api/attendance/{id}` | Get single record |
| PUT | `/api/attendance/{id}` | Update attendance status |
| DELETE | `/api/attendance/{id}` | Delete record |

### POST `/api/attendance/`

**Request body**
```json
{
  "employee_id": "uuid-of-employee",
  "date": "2025-03-10",
  "status": "Present"
}
```

**Status values:** `Present` | `Absent` | `Late` | `Half Day`

**Responses**
- `201` – Marked
- `404` – Employee not found
- `409` – Already marked for that date
- `422` – Future date or invalid status

### GET `/api/attendance/`

**Query params**
| Param | Type | Description |
|-------|------|-------------|
| `employee_id` | string | Filter by employee UUID |
| `from_date` | date | Start of date range (YYYY-MM-DD) |
| `to_date` | date | End of date range (YYYY-MM-DD) |
| `status` | string | Filter by status value |

### PUT `/api/attendance/{id}`

```json
{ "status": "Late" }
```

---

## Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/stats` | Full stats for dashboard |

**Response**
```json
{
  "total_employees": 25,
  "total_departments": 4,
  "attendance_rate": 87.5,
  "today": {
    "present": 18,
    "absent": 3,
    "late": 2,
    "half_day": 1,
    "marked": 24,
    "unmarked": 1
  },
  "department_breakdown": [
    { "department": "Engineering", "count": 10 }
  ],
  "recent_employees": [
    { "id": "uuid", "name": "Kapil Raghav", "employee_id": "EMP001", "department": "Engineering" }
  ]
}
```

---

## Error Format

All errors follow this structure:
```json
{
  "detail": "Human-readable error message"
}
```

Validation errors (422) return:
```json
{
  "detail": [
    { "loc": ["body", "email"], "msg": "value is not a valid email address", "type": "value_error" }
  ]
}
```
