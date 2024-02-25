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

  return (
    <Layout.Header style={headerStyle}>
      {isAuthenticated ? (
        <>
          <Button onClick={logout} style={{ float: "right" }}>
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
