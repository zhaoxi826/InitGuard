import React, { createContext, useContext, useState, useEffect } from 'react';
import api from '../api';
import { jwtDecode } from 'jwt-decode';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('token'));

  useEffect(() => {
    if (token) {
      // Decode token to get user info if needed
      try {
        const payload = jwtDecode(token);
        setUser({ user_id: payload.user_id });
      } catch (e) {
        console.error("Invalid token", e);
        logout();
      }
    } else {
        setUser(null);
    }
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await api.post('/auth/login', { username, password });
      const newToken = response.data.token;
      localStorage.setItem('token', newToken);
      setToken(newToken);
      return true;
    } catch (error) {
      console.error("Login failed", error);
      throw error;
    }
  };

  const register = async (username, email, password) => {
    try {
      await api.post('/auth/register', { username, email, password });
      return true;
    } catch (error) {
        console.error("Registration failed", error);
        throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
