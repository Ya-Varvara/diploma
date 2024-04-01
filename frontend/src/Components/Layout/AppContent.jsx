import { Layout, Button, theme, Breadcrumb } from "antd";
import { useAuth } from "../../AuthContext";

const contentStyle = {
  textAlign: "center",
  minHeight: "calc(100vh - 60px)",
  color: "#666",
  backgroundColor: "#ffffff",
  padding: "1rem",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
};

export default function AppContent({ children }) {
  const { isAuthenticated } = useAuth();

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();
  // console.log(isAuthenticated);

  if (isAuthenticated) {
    return (
      <Layout.Content
        style={{
          padding: "0 48px",
        }}
      >
        <Breadcrumb
          style={{
            margin: "16px 0",
          }}
        >
          <Breadcrumb.Item>Home</Breadcrumb.Item>
          <Breadcrumb.Item>List</Breadcrumb.Item>
          <Breadcrumb.Item>App</Breadcrumb.Item>
        </Breadcrumb>
        <div
          style={{
            padding: 24,
            minHeight: "85vh",
            background: colorBgContainer,
            borderRadius: borderRadiusLG,
          }}
        >
          {children}
        </div>
      </Layout.Content>
    );
  } else {
    return <Layout.Content style={contentStyle}>{children}</Layout.Content>;
  }
}
