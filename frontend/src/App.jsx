import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import CreateResource from './pages/CreateResource';
import CreateTask from './pages/CreateTask';
import Layout from './components/Layout';

const ProtectedRoute = ({ children }) => {
  const { user, token } = useAuth();
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/resource/create"
          element={
            <ProtectedRoute>
              <CreateResource />
            </ProtectedRoute>
          }
        />
        <Route
          path="/task/create"
          element={
            <ProtectedRoute>
              <CreateTask />
            </ProtectedRoute>
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
