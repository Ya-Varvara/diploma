import React, { createContext, useContext, useState, useEffect } from "react";
import Cookies from "js-cookie";
// import { useNavigate } from "react-router-dom"; // Для навигации

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  // const navigate = useNavigate();

  useEffect(() => {
    const isAuthenticatedCookie = Cookies.get("auth_cookie");
    console.log(isAuthenticatedCookie);
    if (isAuthenticatedCookie) {
      setIsAuthenticated(true);
    }
  }, []);

  const login = () => {
    setIsAuthenticated(true);
    // Устанавливаем куку "cookie" при входе
    Cookies.set("auth_cookie", "true", { expires: 1 }); // Кука будет сохраняться 7 дней
  };

  const logout = () => {
    setIsAuthenticated(false);
    // Удаляем куку "cookie" при выходе
    Cookies.remove("auth_cookie");
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
