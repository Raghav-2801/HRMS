from datetime import date, timedelta


class TestDashboard:
    def test_empty_dashboard(self, client):
        resp = client.get("/api/dashboard/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_employees"] == 0
        assert data["total_departments"] == 0
        assert data["attendance_rate"] == 0.0
        assert data["today"]["present"] == 0
        assert data["today"]["unmarked"] == 0

    def test_dashboard_with_data(self, client, sample_employee, sample_employee_2):
        today = date.today()
        # Mark one present today
        client.post("/api/attendance/", json={
            "employee_id": sample_employee["id"],
            "date": str(today),
            "status": "Present",
        })
        resp = client.get("/api/dashboard/stats")
        assert resp.status_code == 200
        data = resp.json()
        assert data["total_employees"] == 2
        assert data["total_departments"] == 2  # Engineering + HR
        assert data["today"]["present"] == 1
        assert data["today"]["unmarked"] == 1  # sample_employee_2 not marked

    def test_department_breakdown(self, client, sample_employee, sample_employee_2):
        resp = client.get("/api/dashboard/stats")
        data = resp.json()
        depts = {d["department"]: d["count"] for d in data["department_breakdown"]}
        assert depts.get("Engineering") == 1
        assert depts.get("HR") == 1

    def test_recent_employees(self, client, sample_employee, sample_employee_2):
        resp = client.get("/api/dashboard/stats")
        data = resp.json()
        assert len(data["recent_employees"]) == 2

    def test_health_check(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
