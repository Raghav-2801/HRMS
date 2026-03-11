from datetime import date, timedelta
import pytest


def mark(client, emp_id, status="Present", days_ago=1):
    day = date.today() - timedelta(days=days_ago)
    return client.post("/api/attendance/", json={
        "employee_id": emp_id,
        "date": str(day),
        "status": status,
    })


class TestMarkAttendance:
    def test_mark_present(self, client, sample_employee):
        resp = mark(client, sample_employee["id"], "Present")
        assert resp.status_code == 201
        data = resp.json()
        assert data["status"] == "Present"
        assert data["employee_name"] == "Kapil Raghav"

    def test_mark_absent(self, client, sample_employee):
        resp = mark(client, sample_employee["id"], "Absent")
        assert resp.status_code == 201

    def test_mark_late(self, client, sample_employee):
        resp = mark(client, sample_employee["id"], "Late")
        assert resp.status_code == 201

    def test_mark_half_day(self, client, sample_employee):
        resp = mark(client, sample_employee["id"], "Half Day")
        assert resp.status_code == 201

    def test_duplicate_attendance(self, client, sample_employee):
        emp_id = sample_employee["id"]
        mark(client, emp_id, "Present", days_ago=2)
        resp = mark(client, emp_id, "Absent", days_ago=2)  # same date
        assert resp.status_code == 409

    def test_future_date_rejected(self, client, sample_employee):
        future = date.today() + timedelta(days=1)
        resp = client.post("/api/attendance/", json={
            "employee_id": sample_employee["id"],
            "date": str(future),
            "status": "Present",
        })
        assert resp.status_code == 422

    def test_nonexistent_employee(self, client):
        resp = client.post("/api/attendance/", json={
            "employee_id": "nonexistent",
            "date": str(date.today() - timedelta(days=1)),
            "status": "Present",
        })
        assert resp.status_code == 404

    def test_invalid_status(self, client, sample_employee):
        resp = client.post("/api/attendance/", json={
            "employee_id": sample_employee["id"],
            "date": str(date.today() - timedelta(days=1)),
            "status": "OnLeave",  # invalid
        })
        assert resp.status_code == 422


class TestListAttendance:
    def test_list_all(self, client, sample_employee, sample_employee_2):
        mark(client, sample_employee["id"], "Present", 1)
        mark(client, sample_employee_2["id"], "Absent", 2)
        resp = client.get("/api/attendance/")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    def test_filter_by_employee(self, client, sample_employee, sample_employee_2):
        mark(client, sample_employee["id"], "Present", 1)
        mark(client, sample_employee_2["id"], "Absent", 2)
        resp = client.get(f"/api/attendance/?employee_id={sample_employee['id']}")
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    def test_filter_by_status(self, client, sample_employee, sample_employee_2):
        mark(client, sample_employee["id"], "Present", 1)
        mark(client, sample_employee_2["id"], "Absent", 2)
        resp = client.get("/api/attendance/?status=Present")
        assert resp.status_code == 200
        data = resp.json()
        assert all(r["status"] == "Present" for r in data)

    def test_filter_by_date_range(self, client, sample_employee):
        mark(client, sample_employee["id"], "Present", 1)
        mark(client, sample_employee["id"], "Late", 5)
        from_date = date.today() - timedelta(days=3)
        resp = client.get(f"/api/attendance/?from_date={from_date}")
        assert resp.status_code == 200
        assert len(resp.json()) == 1


class TestTodayAttendance:
    def test_today_empty(self, client, sample_employee):
        resp = client.get("/api/attendance/today")
        assert resp.status_code == 200
        assert resp.json() == []

    def test_today_with_record(self, client, sample_employee):
        today = date.today()
        client.post("/api/attendance/", json={
            "employee_id": sample_employee["id"],
            "date": str(today),
            "status": "Present",
        })
        resp = client.get("/api/attendance/today")
        assert resp.status_code == 200
        assert len(resp.json()) == 1


class TestUpdateAttendance:
    def test_update_status(self, client, sample_employee):
        resp = mark(client, sample_employee["id"], "Present")
        att_id = resp.json()["id"]
        update = client.put(f"/api/attendance/{att_id}", json={"status": "Late"})
        assert update.status_code == 200
        assert update.json()["status"] == "Late"

    def test_update_nonexistent(self, client):
        resp = client.put("/api/attendance/bad-id", json={"status": "Present"})
        assert resp.status_code == 404


class TestDeleteAttendance:
    def test_delete_record(self, client, sample_employee):
        resp = mark(client, sample_employee["id"], "Present")
        att_id = resp.json()["id"]
        del_resp = client.delete(f"/api/attendance/{att_id}")
        assert del_resp.status_code == 204
        assert client.get(f"/api/attendance/{att_id}").status_code == 404

    def test_delete_nonexistent(self, client):
        resp = client.delete("/api/attendance/bad-id")
        assert resp.status_code == 404


class TestCascadeDelete:
    def test_attendance_deleted_when_employee_deleted(self, client, sample_employee):
        mark(client, sample_employee["id"], "Present", 1)
        mark(client, sample_employee["id"], "Absent", 2)
        # Delete employee
        client.delete(f"/api/employees/{sample_employee['id']}")
        # All attendance should be gone
        resp = client.get("/api/attendance/")
        assert len(resp.json()) == 0
