import { Layout, Button } from "antd";
import { useAuth } from "../../AuthContext";
import { MenuFoldOutlined, MenuUnfoldOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom"; // Для навигации

const headerStyle = {
  width: "100%",
  textAlign: "center",
  height: 60,
  padding: "1rem",
  // display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  backgroundColor: "#f5f5f5",
};

export default function AppHeader({ onClick }) {
  const { isAuthenticated, login, logout } = useAuth();
  const navigate = useNavigate();

  function loginClick() {
    navigate("/login")
  }

  function logoutClick() {
    // Отправляем запрос на сервер для выхода из системы
    fetch('http://localhost:8000/auth/logout', {
      method: 'POST', // или 'GET', в зависимости от того, как ожидает ваш сервер
      credentials: 'include', // если используются cookies
    })
    .then(response => {
      if (response.ok) {
        console.log("Вы успешно вышли из системы");
        logout(); // очистка данных аутентификации на клиенте
        navigate("/"); // перенаправление на страницу входа
      } else {
        throw new Error('Проблема при выходе из системы');
      }
    })
    .catch(error => {
      console.error(error.message);
    });
  }

  return (
    <Layout.Header style={headerStyle}>
      {isAuthenticated ? (
        <>
          <Button onClick={logoutClick} style={{ float: "right" }}>
            Выйти
          </Button>
        </>
      ) : (
        <Button onClick={loginClick} style={{ float: "right" }}>
          Войти
        </Button>
      )}
    </Layout.Header>
  );
}
