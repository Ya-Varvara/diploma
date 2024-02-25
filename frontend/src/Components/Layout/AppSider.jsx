import { Layout } from "antd";

const siderStyle = {
  textAlign: "center",
  lineHeight: "120px",
  color: "#fff",
  backgroundColor: "#1677ff",
};

export default function AppSider({siderState}) {
  // console.log(siderState)
  return (
    <Layout.Sider width="25%" style={siderStyle} trigger={null} collapsible collapsed={siderState}>
      Sider
    </Layout.Sider>
  );
}
