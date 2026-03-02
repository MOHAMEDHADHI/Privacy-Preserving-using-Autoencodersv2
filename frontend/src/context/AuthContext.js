import React, { createContext, useState, useContext, useEffect } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in (from localStorage)
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
    setLoading(false);
  }, []);

  const login = (email, password) => {
    // Simple demo authentication
    // In production, this would call your backend API
    const demoUser = {
      id: 1,
      email: email,
      name: email.split('@')[0],
    };
    
    setUser(demoUser);
    localStorage.setItem('user', JSON.stringify(demoUser));
    return Promise.resolve(demoUser);
  };

  const register = (email, password) => {
    // Simple demo registration
    const newUser = {
      id: Date.now(),
      email: email,
      name: email.split('@')[0],
    };
    
    setUser(newUser);
    localStorage.setItem('user', JSON.stringify(newUser));
    return Promise.resolve(newUser);
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('user');
  };

  const value = {
    user,
    login,
    register,
    logout,
    loading,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
