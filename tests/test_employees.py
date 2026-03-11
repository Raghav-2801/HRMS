import pytest


class TestCreateEmployee:
    def test_create_employee_success(self, client):
        payload = {
            "employee_id": "EMP001",
            "name": "Kapil Raghav",
            "email": "kapil@example.com",
            "department": "Engineering",
        }
        resp = client.post("/api/employees/", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["employee_id"] == "EMP001"
        assert data["name"] == "Kapil Raghav"
        assert data["email"] == "kapil@example.com"
        assert "id" in data

    def test_create_employee_duplicate_id(self, client, sample_employee):
        payload = {
            "employee_id": "EMP001",
            "name": "Someone Else",
            "email": "other@example.com",
            "department": "HR",
        }
        resp = client.post("/api/employees/", json=payload)
        assert resp.status_code == 409
        assert "EMP001" in resp.json()["detail"]

    def test_create_employee_duplicate_email(self, client, sample_employee):
        payload = {
            "employee_id": "EMP999",
            "name": "Someone Else",
            "email": "kapil@example.com",  # duplicate
            "department": "HR",
        }
        resp = client.post("/api/employees/", json=payload)
        assert resp.status_code == 409

    def test_create_employee_invalid_email(self, client):
        payload = {
            "employee_id": "EMP002",
            "name": "Test User",
            "email": "not-an-email",
            "department": "IT",
        }
        resp = client.post("/api/employees/", json=payload)
        assert resp.status_code == 422

    def test_create_employee_missing_fields(self, client):
        resp = client.post("/api/employees/", json={"name": "No ID"})
        assert resp.status_code == 422


class TestListEmployees:
    def test_list_all_employees(self, client, sample_employee, sample_employee_2):
        resp = client.get("/api/employees/")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_search_by_name(self, client, sample_employee, sample_employee_2):
        resp = client.get("/api/employees/?search=Kapil")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["name"] == "Kapil Raghav"

    def test_filter_by_department(self, client, sample_employee, sample_employee_2):
        resp = client.get("/api/employees/?department=Engineering")
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) == 1
        assert data[0]["department"] == "Engineering"

    def test_list_departments(self, client, sample_employee, sample_employee_2):
        resp = client.get("/api/employees/departments")
        assert resp.status_code == 200
        depts = resp.json()
        assert "Engineering" in depts
        assert "HR" in depts


class TestGetEmployee:
    def test_get_existing_employee(self, client, sample_employee):
        emp_id = sample_employee["id"]
        resp = client.get(f"/api/employees/{emp_id}")
        assert resp.status_code == 200
        assert resp.json()["id"] == emp_id

    def test_get_nonexistent_employee(self, client):
        resp = client.get("/api/employees/nonexistent-id")
        assert resp.status_code == 404


class TestUpdateEmployee:
    def test_update_employee_name(self, client, sample_employee):
        emp_id = sample_employee["id"]
        resp = client.put(f"/api/employees/{emp_id}", json={"name": "Kapil Updated"})
        assert resp.status_code == 200
        assert resp.json()["name"] == "Kapil Updated"

    def test_update_employee_department(self, client, sample_employee):
        emp_id = sample_employee["id"]
        resp = client.put(f"/api/employees/{emp_id}", json={"department": "DevOps"})
        assert resp.status_code == 200
        assert resp.json()["department"] == "DevOps"

    def test_update_email_conflict(self, client, sample_employee, sample_employee_2):
        emp_id = sample_employee["id"]
        resp = client.put(f"/api/employees/{emp_id}", json={"email": "rahul@example.com"})
        assert resp.status_code == 409

    def test_update_nonexistent_employee(self, client):
        resp = client.put("/api/employees/bad-id", json={"name": "Ghost"})
        assert resp.status_code == 404


class TestDeleteEmployee:
    def test_delete_employee(self, client, sample_employee):
        emp_id = sample_employee["id"]
        resp = client.delete(f"/api/employees/{emp_id}")
        assert resp.status_code == 204
        # Verify deleted
        assert client.get(f"/api/employees/{emp_id}").status_code == 404

    def test_delete_nonexistent_employee(self, client):
        resp = client.delete("/api/employees/bad-id")
        assert resp.status_code == 404


class TestEmployeeSummary:
    def test_summary_no_attendance(self, client, sample_employee):
        emp_id = sample_employee["id"]
        resp = client.get(f"/api/employees/{emp_id}/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_days"] == 0
        assert data["attendance_rate"] == 0.0

    def test_summary_with_attendance(self, client, sample_employee):
        emp_id = sample_employee["id"]
        from datetime import date, timedelta
        # Mark 2 present, 1 absent
        for i in range(3):
            day = date.today() - timedelta(days=i + 1)
            status = "Present" if i < 2 else "Absent"
            client.post("/api/attendance/", json={
                "employee_id": emp_id, "date": str(day), "status": status
            })
        resp = client.get(f"/api/employees/{emp_id}/summary")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_days"] == 3
        assert data["present"] == 2
        assert data["absent"] == 1
