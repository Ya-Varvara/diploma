import { Layout, Button, Space } from "antd";
import { useAuth } from "../../AuthContext";
import { useNavigate } from "react-router-dom"; // Для навигации

export default function AppHeader() {
  const { isAuthenticated, login, logout } = useAuth();
  const navigate = useNavigate();

  function loginClick() {
    navigate("/login");
  }

  function logoutClick() {
    // Отправляем запрос на сервер для выхода из системы
    fetch("http://localhost:8000/auth/logout", {
      method: "POST", // или 'GET', в зависимости от того, как ожидает ваш сервер
      credentials: "include", // если используются cookies
    })
      .then((response) => {
        if (response.ok) {
          console.log("Вы успешно вышли из системы");
          logout(); // очистка данных аутентификации на клиенте
          navigate("/home"); // перенаправление на страницу входа
        } else {
          throw new Error("Проблема при выходе из системы");
        }
      })
      .catch((error) => {
        console.error(error.message);
      });
  }

  return (
    <Layout.Header
      style={{
        // position: "sticky",
        top: 0,
        zIndex: 1,
        width: "100%",
        display: "flex",
        alignItems: "center",
      }}
    >
      {isAuthenticated ? (
        <>
          <Space size="small"> </Space>
          <Button onClick={logoutClick} style={{ float: "right" }}>
            Выйти
          </Button>
        </>
      ) : (
        <>
          <Space size="small"> </Space>
          <Button onClick={loginClick} style={{ float: "right" }}>
            Войти
          </Button>
        </>
      )}
    </Layout.Header>
  );
}
