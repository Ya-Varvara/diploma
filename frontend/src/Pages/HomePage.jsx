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
import OneTestView from "./TestPage";

import { FetchTests, FetchTaskTypes } from "../Handlers/API";

export default function HomePage() {
  const { isAuthenticated } = useAuth();

  const [taskTypeFormVisible, setTaskTypeFormVisible] = useState(false);
  const [TestFormVisible, setTestFormVisible] = useState(false);

  const [tests, setTests] = useState([]);
  const [task_types, setTaskTypes] = useState([]);
  useEffect(() => {
    FetchTests({ setter: setTests });
    FetchTaskTypes({ setter: setTaskTypes });
  }, []);

  return (
    <Layout
      style={{
        minHeight: "100vh",
      }}
    >
      <AppHeader />
      <Layout>
        <AppContent>
          {isAuthenticated ? (
            <>
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
              {/* <ViewTable data={tests} type="test" /> */}
              {/* <ViewTable data={task_types} type="task_type" /> */}
              <OneTestView test_id={2} />
            </>
          ) : (
            <MainUnauthorizedPage />
          )}
        </AppContent>
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
