import React from "react";
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { Col, Row, Card, Space, Typography, List } from "antd";

import { FetchTaskTypeByID } from "../Handlers/API";

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
    <Card title="Информация о типах заданий">
      <List>
        <List.Item>
          <Title level={5}>Название теста:</Title>
          <Text>{info.name}</Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Базовый тип:</Title>
          <Text>Нет</Text>
        </List.Item>
        {/* <List.Item>
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
        </List.Item> */}
        {/* <List.Item>
          <Title level={5}>Типы заданий:</Title>
          <Text>{taskTypesList}</Text>
        </List.Item> */}
      </List>
    </Card>
  );
};

export default function OneTaskTypePage({ test_id }) {
  const { id } = useParams();
  console.log("From path: ", id);
  const [info, setInfo] = useState({});

  useEffect(() => {
    FetchTaskTypeByID({ setter: setInfo, id: id });
    console.log("Info: ", info);
  }, []);

  return (
    <BasePage>
        <Col span={12}>
          <TestInfo info={info} />
        </Col>
    </BasePage>
  );
};

