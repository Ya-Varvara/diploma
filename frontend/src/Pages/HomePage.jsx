import React, { useEffect } from "react";
import { useState } from "react";
import { Layout, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../AuthContext";
import MainUnauthorizedPage from "../Components/MainUnauthorizedPage";
import CreateTaskTypeForm from "../Components/Forms/CreateTaskTypeForm";
import CreateTestForm from "../Components/Forms/CreateTestForm";
import BasePage from "../Components/Layout/BasePage";

export default function HomePage() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  if (!isAuthenticated) {
    return (
      <BasePage>
        <MainUnauthorizedPage />
      </BasePage>
    );
  }

  return (
    <BasePage>
      Welcome!
      <Button type="primary" onClick={() => navigate(`/home/tests/`)}>
        Тесты
      </Button>
      <Button type="primary" onClick={() => navigate(`/home/task_types/`)}>
        Типы заданий
      </Button>
    </BasePage>
  );
}
