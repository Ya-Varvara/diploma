import React, { useEffect } from "react";
import { useState } from "react";
import { Layout, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";

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
