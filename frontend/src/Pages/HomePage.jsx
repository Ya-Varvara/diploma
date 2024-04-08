import React, { useEffect } from "react";
import { useState } from "react";
import { Layout, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";

import { useAuth } from "../AuthContext";
import MainUnauthorizedPage from "../Components/MainUnauthorizedPage";
import CreateTaskTypeForm from "../Components/Forms/CreateTaskTypeForm";
import CreateTestForm from "../Components/Forms/CreateTestForm";
import BasePage from "../Components/Layout/BasePage";

export default function HomePage() {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return (
      <BasePage>
        <MainUnauthorizedPage />
      </BasePage>
    );
  }

  return <BasePage>Welcome!</BasePage>;
}
