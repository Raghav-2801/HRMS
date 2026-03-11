import axios from 'axios'

const BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({ baseURL: BASE })

// ── Employees ──
export const getEmployees = (params) => api.get('/api/employees/', { params })
export const getEmployee = (id) => api.get(`/api/employees/${id}`)
export const createEmployee = (data) => api.post('/api/employees/', data)
export const updateEmployee = (id, data) => api.put(`/api/employees/${id}`, data)
export const deleteEmployee = (id) => api.delete(`/api/employees/${id}`)
export const getDepartments = () => api.get('/api/employees/departments')
export const getEmployeeSummary = (id) => api.get(`/api/employees/${id}/summary`)

// ── Attendance ──
export const getAttendance = (params) => api.get('/api/attendance/', { params })
export const getTodayAttendance = () => api.get('/api/attendance/today')
export const markAttendance = (data) => api.post('/api/attendance/', data)
export const updateAttendance = (id, data) => api.put(`/api/attendance/${id}`, data)
export const deleteAttendance = (id) => api.delete(`/api/attendance/${id}`)

// ── Dashboard ──
export const getDashboardStats = () => api.get('/api/dashboard/stats')
