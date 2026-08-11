import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiService } from '../api/client';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const saved = localStorage.getItem('agri_user');
    return saved ? JSON.parse(saved) : null;
  });

  const signIn = async (userPayload) => {
    const emailOrPhone = userPayload.emailOrPhone || 'ramesh.farmer@agrisaarthi.in';
    let profile = null;
    
    if (!userPayload.isDemo) {
      try {
        profile = await apiService.getFarmerProfile(emailOrPhone);
      } catch (e) {
        console.warn("Failed to get profile from backend:", e);
      }
    }

    const farmerUser = {
      name: profile?.name || userPayload.name || 'Ramesh Kumar',
      location: profile?.location || userPayload.location || 'Meerut, Uttar Pradesh',
      emailOrPhone: emailOrPhone,
      landholding: profile?.land_size || userPayload.landholding || '2.5 Acres',
      soilType: profile?.soil_type || userPayload.soilType || 'Alluvial Soil',
      isDemo: Boolean(userPayload.isDemo),
      signedInAt: new Date().toISOString()
    };

    // Sync to backend database
    if (!userPayload.isDemo) {
      try {
        await apiService.saveFarmerProfile(farmerUser);
      } catch (e) {
        console.warn("Failed to save profile on backend:", e);
      }
    }

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
