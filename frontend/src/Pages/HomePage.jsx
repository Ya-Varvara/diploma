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

  return (
    <BasePage>
      Welcome!
    </BasePage>
  );
}

  // const [taskTypeFormVisible, setTaskTypeFormVisible] = useState(false);
  // const [TestFormVisible, setTestFormVisible] = useState(false);
{/* <Button
        name="taskTypeForm"
        type="primary"
        onClick={() => setTaskTypeFormVisible(true)}
        icon={<PlusOutlined />}
      >
        Новый тип задания
      </Button>
      <CreateTaskTypeForm
        open={taskTypeFormVisible}
        onClose={() => setTaskTypeFormVisible(false)}
      />
      <Button
        name="testForm"
        type="primary"
        onClick={() => setTestFormVisible(true)}
        icon={<PlusOutlined />}
      >
        Новая контрольная
      </Button>
      <CreateTestForm
        open={TestFormVisible}
        onClose={() => setTestFormVisible(false)}
      /> */}
      // <ViewTable data={tests} type="test" />
      // <ViewTable data={task_types} type="task_type" />
      //  <OneTestView test_id={2} />