import React, { useEffect, useState } from "react";

import ViewTable from "../Components/Forms/Table";
import { FetchTaskTypes } from "../Handlers/API";
import BasePage from "../Components/Layout/BasePage";
import CreateTaskTypeForm from "../Components/Forms/CreateTaskTypeForm";

import { Space, Row, Col, Button } from "antd";
import { PlusOutlined } from "@ant-design/icons";

export default function AllTaskTypesPage() {
  const [types, setTypes] = useState([]);
  const [taskTypeFormVisible, setTaskTypeFormVisible] = useState(false);

  useEffect(() => {
    FetchTaskTypes({ setter: setTypes });
  }, []);

  return (
    <BasePage>
      <Space direction="vertical" size="large" style={{ display: "flex" }}>
        <Row justify="space-between" style={{ width: "100%" }}>
          <Col span={18}>
            <h2>Все типы заданий</h2>
          </Col>
          <Col span={6}>
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
          </Col>
        </Row>
        <ViewTable type="task_type" data={types} />
      </Space>
    </BasePage>
  );
}
