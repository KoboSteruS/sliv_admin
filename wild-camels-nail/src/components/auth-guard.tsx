/**
 * Компонент для проверки авторизации
 */
import { useEffect } from "react";
import { useNavigate, useLocation } from "react-router";
import { Outlet } from "react-router";

export const AuthGuard = () => {
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    // Проверяем наличие токена
    const token = localStorage.getItem("auth_token");
    
    // Если токена нет и мы не на странице логина - перенаправляем
    if (!token && location.pathname !== "/login") {
      navigate("/login");
    }
    
    // Если токен есть и мы на странице логина - перенаправляем на главную
    if (token && location.pathname === "/login") {
      navigate("/products");
    }
  }, [navigate, location.pathname]);

  return <Outlet />;
};

