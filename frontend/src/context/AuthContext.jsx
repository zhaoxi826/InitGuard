import React, { createContext, useContext, useState } from 'react';
import { jwtDecode } from 'jwt-decode';
import api from '../api';

const AuthContext = createContext();

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(() => {
    const t = localStorage.getItem('token');
    if (t) {
      try {
        jwtDecode(t);
        return t;
      } catch {
        localStorage.removeItem('token');
        return null;
      }
    }
    return null;
  });

  const [user, setUser] = useState(() => {
    if (token) {
      try {
        const payload = jwtDecode(token);
        return { user_id: payload.user_id };
      } catch {
        return null;
      }
    }
    return null;
  });

  const logout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setUser(null);
  };

  const login = async (username, password) => {
    try {
      const response = await api.post('/auth/login', { username, password });
      const newToken = response.data.token;
      localStorage.setItem('token', newToken);
      setToken(newToken);
      try {
        const payload = jwtDecode(newToken);
        setUser({ user_id: payload.user_id });
      } catch (e) {
        console.error("Invalid token received", e);
        logout();
      }
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

  return (
    <AuthContext.Provider value={{ user, token, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
