import { createContext, useState, useEffect } from "react";
import { loginUser, logoutUser } from "../api/auth";
import axiosInstance, { setAccessToken } from "../api/axiosInstance";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  const login = async (credentials) => {
    await loginUser(credentials);
    setIsAuthenticated(true);
  };

  const logout = async () => {
    await logoutUser();
    setIsAuthenticated(false);
  };

  // Restore session on load
  useEffect(() => {
    const initAuth = async () => {
      try {
        const res = await axiosInstance.post("/token/refresh/");

        setAccessToken(res.data.access);
        setIsAuthenticated(true);
      } catch {
        setIsAuthenticated(false);
      } finally {
        setLoading(false);
      }
    };

    initAuth();
  }, []);

  const contextData = {
    isAuthenticated,
    login,
    logout,
    loading,
  };

  return (
    <AuthContext.Provider value={contextData}>
      {children}
    </AuthContext.Provider>
  );
};