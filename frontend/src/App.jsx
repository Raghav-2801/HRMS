import { BrowserRouter as Router, Routes, Route, NavLink } from 'react-router-dom';
import './styles.css';

import Dashboard from './components/Dashboard';
import EmployeeList from './components/EmployeeList';
import AddEmployee from './components/AddEmployee';
import Attendance from './components/Attendance';

function App() {
  return (
    <Router>
      <nav className="navbar">
        <h1> HRMS Lite</h1>
        <div className="nav-links">
          <NavLink to="/" end>Dashboard</NavLink>
          <NavLink to="/employees">Employees</NavLink>
          <NavLink to="/add">Add Employee</NavLink>
          <NavLink to="/attendance">Attendance</NavLink>
        </div>
      </nav>

      <div className="container">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/employees" element={<EmployeeList />} />
          <Route path="/add" element={<AddEmployee />} />
          <Route path="/attendance" element={<Attendance />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
