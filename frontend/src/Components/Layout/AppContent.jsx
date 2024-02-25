import { Layout, Button } from "antd";
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
  // console.log(isAuthenticated);

  return <Layout.Content style={contentStyle}> {children} </Layout.Content>;
};
