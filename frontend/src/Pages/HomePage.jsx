import React from "react";
import { Button, Space, Row, Col, Typography, Divider } from "antd";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../AuthContext";
import MainUnauthorizedPage from "../Components/MainUnauthorizedPage";
import BasePage from "../Components/Layout/BasePage";

const { Title, Text } = Typography;

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
      <Space direction="vertical" size="large" style={{ display: "flex" }}>
        <Row>
          <Col span={24}>
            <Title level={1}>Добро пожаловать!</Title>
          </Col>
        </Row>
        <Row>
          <Col span={24}>
            <Text>
              Это приложение предназначено для создания тестирований для курса
              "Дискретная математика"
            </Text>
          </Col>
        </Row>
        <Divider />
        <Row>
          {/* <Space size="large"> */}
          <Col span={6}>
            <Button
              type="default"
              style={{ height: "100px", borderRadius: 0 }}
              block
            />
          </Col>
          <Col span={6}>
            <Button
              type="default"
              onClick={() => navigate(`/home/tests/`)}
              style={{ height: "100px", borderRadius: 0 }}
              block
            >
              Тесты
            </Button>
          </Col>
          <Col span={6}>
            <Button
              type="default"
              onClick={() => navigate(`/home/task_types/`)}
              style={{ height: "100px", borderRadius: 0 }}
              block
            >
              Типы заданий
            </Button>
          </Col>
          <Col span={6}>
            <Button
              type="default"
              style={{ height: "100px", borderRadius: 0 }}
              block
            />
          </Col>
          {/* </Space> */}
        </Row>
      </Space>
    </BasePage>
  );
}
