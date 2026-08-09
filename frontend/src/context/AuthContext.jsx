import React, { createContext, useContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('agri_user');
    return saved ? JSON.parse(saved) : null;
  });

  const signIn = (userPayload) => {
    const farmerUser = {
      name: userPayload.name || 'Ramesh Kumar',
      location: userPayload.location || 'Meerut, Uttar Pradesh',
      emailOrPhone: userPayload.emailOrPhone || 'ramesh.farmer@agrisaarthi.in',
      landholding: '2.5 Acres',
      soilType: 'Alluvial Soil',
      signedInAt: new Date().toISOString()
    };
    setUser(farmerUser);
    localStorage.setItem('agri_user', JSON.stringify(farmerUser));
  };

  const signOut = () => {
    setUser(null);
    localStorage.removeItem('agri_user');
  };

  return (
    <AuthContext.Provider value={{ user, signIn, signOut, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
