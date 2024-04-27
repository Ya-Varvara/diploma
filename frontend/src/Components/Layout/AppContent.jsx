import React from "react";
import { Layout, theme, Breadcrumb } from "antd";
import { useLocation, Link } from "react-router-dom";
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

const breadcrumbNameMap = {
  home: "Главная",
  tests: "Тесты",
  task_types: "Типы заданий",
};

const createBreadcrumbItems = (pathname) => {
  const paths = pathname.split("/").filter((x) => x);
  const items = [];
  let pathAccum = "";
  let prevItem = "";

  paths.forEach((path, index) => {
    pathAccum += `/${path}`;
    if (path !== "variant") {
      const isLast = index === paths.length - 1;
      let breadcrumbName;

      if (prevItem === "tests") {
        breadcrumbName = `Тест ${path}`;
      } else if (prevItem === "variant") {
        breadcrumbName = `Вариант ${path}`;
      } else {
        breadcrumbName = breadcrumbNameMap[path] || path;
      }
      console.log(path, breadcrumbName);
      items.push(
        <Breadcrumb.Item key={pathAccum}>
          {isLast ? (
            breadcrumbName
          ) : (
            <Link to={pathAccum}>{breadcrumbName}</Link>
          )}
        </Breadcrumb.Item>
      );
    }
    prevItem = path;
  });
  console.log(items);
  return items;
};

const createBreadcrumb = (pathname) => {
  const paths = pathname.split("/").filter((x) => x);
  const items = paths.map((path, index, arr) => {
    const url = `/${arr.slice(0, index + 1).join("/")}`;
    const isLast = index === paths.length - 1;
    return (
      <Breadcrumb.Item key={url}>
        {isLast ? path : <Link to={url}>{path}</Link>}
      </Breadcrumb.Item>
    );
  });
  return items;
};

export default function AppContent({ children }) {
  const { isAuthenticated } = useAuth();
  const { pathname } = useLocation();
  const breadcrumbItems = createBreadcrumbItems(pathname);

  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

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
          {breadcrumbItems}
        </Breadcrumb>
        <div
          style={{
            textAlign: "center",
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
