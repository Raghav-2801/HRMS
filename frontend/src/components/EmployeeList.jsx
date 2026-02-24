import { useEffect, useState } from 'react';
import { api } from '../api';

function EmployeeList() {
  const [employees, setEmployees] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchEmployees();
  }, []);

  const fetchEmployees = async () => {
    try {
      setLoading(true);
      const response = await api.get('/employees');
      setEmployees(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch employees. Is the backend running?');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this employee?')) return;
    
    try {
      await api.delete(`/employees/${id}`);
      setEmployees(employees.filter((emp) => emp.id !== id));
    } catch (err) {
      alert('Failed to delete employee');
    }
  };

  if (loading) return <div className="loading">Loading employees...</div>;

  return (
    <div className="card">
      <h2>All Employees</h2>
      
      {error && <div className="alert alert-error">{error}</div>}
      
      {employees.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">👥</div>
          <p>No employees found. Add your first employee!</p>
        </div>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Employee ID</th>
              <th>Full Name</th>
              <th>Email</th>
              <th>Department</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {employees.map((emp) => (
              <tr key={emp.id}>
                <td><strong>{emp.employee_id}</strong></td>
                <td>{emp.full_name}</td>
                <td>{emp.email}</td>
                <td>
                  <span className="badge" style={{ background: '#e0e7ff', color: '#4338ca' }}>
                    {emp.department}
                  </span>
                </td>
                <td>
                  <button 
                    className="btn btn-danger" 
                    onClick={() => handleDelete(emp.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default EmployeeList;
