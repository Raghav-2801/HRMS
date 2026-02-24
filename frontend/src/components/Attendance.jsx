import { useEffect, useState } from 'react';
import { api } from '../api';

function Attendance() {
  const [employees, setEmployees] = useState([]);
  const [records, setRecords] = useState([]);
  const [selectedEmployee, setSelectedEmployee] = useState('');
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [status, setStatus] = useState('Present');
  const [message, setMessage] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [empRes, attRes] = await Promise.all([
        api.get('/employees'),
        api.get('/attendance')
      ]);
      setEmployees(empRes.data);
      setRecords(attRes.data);
    } catch (err) {
      setError('Failed to load data. Is the backend running?');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    setLoading(true);

    if (!selectedEmployee) {
      setError('Please select an employee');
      setLoading(false);
      return;
    }

    try {
      // API expects employee_id as query param and attendance data in body
      await api.post(`/attendance?employee_id=${selectedEmployee}`, {
        date,
        status
      });
      setMessage('Attendance marked successfully!');
      fetchData(); // Refresh records
      
      // Clear message after 3 seconds
      setTimeout(() => setMessage(null), 3000);
    } catch (err) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Failed to mark attendance');
      }
    } finally {
      setLoading(false);
    }
  };

  // Get employee name by id
  const getEmployeeName = (id) => {
    const emp = employees.find(e => e.id === id);
    return emp ? `${emp.full_name} (${emp.employee_id})` : `ID: ${id}`;
  };

  return (
    <div className="two-column">
      {/* Mark Attendance Form */}
      <div className="card">
        <h2>Mark Attendance</h2>
        
        {error && <div className="alert alert-error">{error}</div>}
        {message && <div className="alert alert-success">{message}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Select Employee *</label>
            <select
              value={selectedEmployee}
              onChange={(e) => setSelectedEmployee(e.target.value)}
              required
            >
              <option value="">-- Select Employee --</option>
              {employees.map((emp) => (
                <option key={emp.id} value={emp.id}>
                  {emp.full_name} ({emp.employee_id})
                </option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>Date *</label>
            <input
              type="date"
              value={date}
              onChange={(e) => setDate(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Status *</label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              required
            >
              <option value="Present">Present</option>
              <option value="Absent">Absent</option>
            </select>
          </div>

          <button type="submit" className="btn btn-primary" disabled={loading}>
            {loading ? 'Submitting...' : 'Mark Attendance'}
          </button>
        </form>
      </div>

      {/* Attendance Records */}
      <div className="card">
        <h2>Recent Attendance Records</h2>
        
        {records.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">📋</div>
            <p>No attendance records yet.</p>
          </div>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Employee</th>
                <th>Date</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {records.slice(0, 10).map((rec) => (
                <tr key={rec.id}>
                  <td>{getEmployeeName(rec.employee_id)}</td>
                  <td>{rec.date}</td>
                  <td>
                    <span className={rec.status === 'Present' ? 'badge badge-present' : 'badge badge-absent'}>
                      {rec.status}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
        
        {records.length > 10 && (
          <p style={{ textAlign: 'center', color: '#666', marginTop: '1rem' }}>
            Showing last 10 of {records.length} records
          </p>
        )}
      </div>
    </div>
  );
}

export default Attendance;
