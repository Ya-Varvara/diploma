import React from "react";
import { useState, useEffect } from "react";
import { Col, Row, Card, Space, Typography, List } from "antd";

import { FetchTestByID } from "../Handlers/API";

import BasePage from "../Components/Layout/BasePage";

const TestInfo = ({ info }) => {
  const { Title, Text } = Typography;
  const formatDate = (dateString) => {
    const options = {
      year: "numeric",
      month: "long",
      day: "numeric",
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
    };
    return new Date(dateString).toLocaleDateString("ru-RU", options);
  };

  // Функция для получения списка типов заданий
  //   const taskTypesList = info.task_types.map((taskType) => taskType.type.name).join(", ");

  return (
    <Card title="Информация о тесте">
      <List>
        <List.Item>
          <Title level={5}>Название теста:</Title>
          <Text>{info.name}</Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Время начала:</Title>
          <Text>{formatDate(info.start_datetime)}</Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Время окончания:</Title>
          <Text>{formatDate(info.end_datetime)}</Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Время на выполнение:</Title>
          <Text>{info.test_time}</Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Количество вариантов:</Title>
          <Text>{info.variants_number}</Text>
        </List.Item>
        {/* <List.Item>
          <Title level={5}>Типы заданий:</Title>
          <Text>{taskTypesList}</Text>
        </List.Item> */}
      </List>
    </Card>
  );
};

const OneTestView = ({ test_id }) => {
  const [info, setInfo] = useState({});

  useEffect(() => {
    FetchTestByID({ setter: setInfo, id: test_id });
    console.log("Info: ", info);
  }, []);

  return (
    <BasePage>
      <Row justify="space-between" style={{ width: "100%" }}>
        <Col span={12}>
          <TestInfo info={info} />
        </Col>
        <Col span={12}> РЕШЕНИЯ </Col>
      </Row>
    </BasePage>
  );
};

export default OneTestView;
