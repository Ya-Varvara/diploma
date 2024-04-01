import React from "react";
import { Layout } from "antd";
import { useAuth } from "../../AuthContext";

const siderStyle = {
  textAlign: "center",
  lineHeight: "120px",
  color: "#fff",
  backgroundColor: "#1677ff",
};

export default function AppSider({siderState}) {
  const { isAuthenticated } = useAuth();
  return (
    <Layout.Sider width="25%" style={siderStyle} trigger={null} collapsible collapsed={siderState}>
      Sider
    </Layout.Sider>
  );
}
