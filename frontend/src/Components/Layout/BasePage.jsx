import React, { useEffect } from "react";
import { useState } from "react";
import { Layout, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";

import AppHeader from "./AppHeader";
import AppContent from "./AppContent";
import { useAuth } from "../../AuthContext";
import MainUnauthorizedPage from "../MainUnauthorizedPage";
import CreateTaskTypeForm from "../Forms/CreateTaskTypeForm";
import CreateTestForm from "../Forms/CreateTestForm";
import ViewTable from "../Forms/Table";
import OneTestView from "../../Pages/OneTestPage";

import { FetchTests, FetchTaskTypes } from "../../Handlers/API";

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
