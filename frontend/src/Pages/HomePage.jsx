import React, { useEffect } from "react";
import { useState } from "react";
import { Layout, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";

import AppHeader from "../Components/Layout/AppHeader";
import AppContent from "../Components/Layout/AppContent";
import { useAuth } from "../AuthContext";
import MainUnauthorizedPage from "../Components/MainUnauthorizedPage";
import CreateTaskTypeForm from "../Components/Forms/CreateTaskTypeForm";
import CreateTestForm from "../Components/Forms/CreateTestForm";
import ViewTable from "../Components/Forms/Table";

const FetchTests = async ({ setter }) => {
  try {
    const response = await fetch("http://localhost:8000/test/", {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    setter(data);
  } catch (error) {
    console.error("Error:", error);
  }
};

const FetchTaskTypes = async ({ setter }) => {
  try {
    const response = await fetch("http://localhost:8000/task_type/", {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    const data = await response.json();
    setter(data);
  } catch (error) {
    console.error("Error:", error);
  }
};

export default function HomePage() {
  const { isAuthenticated } = useAuth();

  const [taskTypeFormVisible, setTaskTypeFormVisible] = useState(false);
  const [TestFormVisible, setTestFormVisible] = useState(false);

  const [tests, setTests] = useState([]);
  const [task_types, setTaskTypes] = useState([]);
  useEffect(() => {
    FetchTests({ setter: setTests });
    // console.log(tests);
    FetchTaskTypes({ setter: setTaskTypes });
    // console.log(task_types);
  }, []);

  return (
    <Layout>
      <AppHeader />
      <Layout>
        <AppContent>
          {isAuthenticated ? (
            <>
              <Button
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
              />
              <ViewTable data={tests} type="test" />
              <ViewTable data={task_types} type="task_type" />
            </>
          ) : (
            <MainUnauthorizedPage />
          )}
        </AppContent>
      </Layout>
    </Layout>
  );
}
