import React from "react";
import { Layout } from "antd";

import AppHeader from "./AppHeader";
import AppContent from "./AppContent";

export default function BasePage({ children }) {
  return (
    <Layout
      style={{
        minHeight: "100vh",
      }}
    >
      <AppHeader />

      <Layout>
        <AppContent>{children}</AppContent>
      </Layout>

      <Layout.Footer
        style={{
          textAlign: "center",
        }}
      >
        Created by Ya-Varvara
      </Layout.Footer>
    </Layout>
  );
}
