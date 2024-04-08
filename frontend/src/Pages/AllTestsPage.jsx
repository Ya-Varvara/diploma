import React, { useEffect, useState } from "react";
import { Col, Row, Button, Space } from "antd";
import { PlusOutlined } from "@ant-design/icons";

import ViewTable from "../Components/Forms/Table";
import { FetchTests } from "../Handlers/API";
import BasePage from "../Components/Layout/BasePage";
import CreateTestForm from "../Components/Forms/CreateTestForm";

export default function AllTestsPage() {
  const [tests, setTests] = useState([]);
  const [TestFormVisible, setTestFormVisible] = useState(false);

  useEffect(() => {
    FetchTests({ setter: setTests });
  }, []);

  return (
    <BasePage>
      <Space direction="vertical" size="large" style={{ display: "flex" }}>
        <Row justify="space-between" style={{ width: "100%" }}>
          <Col span={18}>
            <h2>Все тестирования</h2>
          </Col>
          <Col span={6}>
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
          </Col>
        </Row>
        <ViewTable type="test" data={tests} />
      </Space>
    </BasePage>
  );
}
