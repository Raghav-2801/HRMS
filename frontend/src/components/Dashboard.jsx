import { useEffect, useState } from 'react';
import { api, API_BASE_URL } from '../api';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      setLoading(true);
      const [statsRes, empRes] = await Promise.all([
        api.get('/dashboard/stats'),
        api.get('/employees'),
      ]);
      setStats(statsRes.data);
      setEmployees(empRes.data.slice(0, 5)); // Show only first 5 employees
      setError(null);
    } catch (err) {
      const status = err.response?.status;
      const detail = err.response?.data?.detail;
      const message = detail
        ? `Failed to load dashboard data: ${detail}`
        : `Failed to load dashboard data. ${status ? `Status: ${status}. ` : ''}Check backend or CORS.`;
      setError(`${message} API: ${API_BASE_URL}`);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className='loading'>Loading dashboard...</div>;
  if (error) return <div className='alert alert-error'>{error}</div>;

  return (
    <div>
      <h2 style={{ marginBottom: '1.5rem', color: '#444' }}>
        Dashboard Overview
      </h2>

      {/* Stats Cards */}
      <div className='stats-grid'>
        <div className='stat-card'>
          <div className='stat-value'>{stats?.total_employees || 0}</div>
          <div className='stat-label'>Total Employees</div>
        </div>
        <div className='stat-card present'>
          <div className='stat-value'>{stats?.total_present_today || 0}</div>
          <div className='stat-label'>Present Today</div>
        </div>
        <div className='stat-card absent'>
          <div className='stat-value'>{stats?.total_absent_today || 0}</div>
          <div className='stat-label'>Absent Today</div>
        </div>
        <div className='stat-card rate'>
          <div className='stat-value'>{stats?.attendance_rate || 0}%</div>
          <div className='stat-label'>Attendance Rate</div>
        </div>
      </div>

      {/* Recent Employees */}
      <div className='card'>
        <h2>Recent Employees</h2>
        {employees.length === 0 ? (
          <div className='empty-state'>
            <div className='empty-state-icon'>👥</div>
            <p>No employees yet. Add your first employee!</p>
          </div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Employee ID</th>
                <th>Name</th>
                <th>Department</th>
                <th>Email</th>
              </tr>
            </thead>
            <tbody>
              {employees.map((emp) => (
                <tr key={emp.id}>
                  <td>{emp.employee_id}</td>
                  <td>{emp.full_name}</td>
                  <td>{emp.department}</td>
                  <td>{emp.email}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}

export default Dashboard;
