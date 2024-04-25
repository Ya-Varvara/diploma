import React from "react";
import { useParams } from "react-router-dom";
import { useState, useEffect } from "react";
import { Col, Row, Card, Typography, List } from "antd";

import { FetchTestByID, FetchVariantsResult } from "../Handlers/API";
import ViewTable from "../Components/Forms/Table";

import BasePage from "../Components/Layout/BasePage";

const { Paragraph } = Typography;

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

  return (
    <Card title="Информация о тесте">
      <List>
        <List.Item>
          <Title level={5}>Название теста:</Title>
          <Text>{info.name}</Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Время начала:</Title>
          <Text>
            {moment
              .utc(info.start_datetime)
              .local()
              .format("YYYY-MM-DD HH:mm:ss")}
          </Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Время окончания:</Title>
          <Text>
            {moment
              .utc(info.end_datetime)
              .local()
              .format("YYYY-MM-DD HH:mm:ss")}
          </Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Время на выполнение:</Title>
          <Text>{info.test_time}</Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Количество вариантов:</Title>
          <Text>{info.variants_number}</Text>
        </List.Item>
        <List.Item>
          <Title level={5}>ID:</Title>
          <Text>
            <Paragraph copyable>{info.link}</Paragraph>
          </Text>
        </List.Item>
      </List>
    </Card>
  );
};

const OneTestPage = ({}) => {
  const { test_id } = useParams();
  console.log("From path: ", test_id);

  const [info, setInfo] = useState({});
  const [variants, setVariants] = useState([]);

  useEffect(() => {
    FetchTestByID({ setter: setInfo, id: test_id });
    console.log("Info: ", info);
    FetchVariantsResult({ setter: setVariants, test_id: test_id });
    console.log("Variants: ", variants);
  }, []);

  return (
    <BasePage>
      <Row justify="space-between" style={{ width: "100%" }}>
        <Col span={8}>
          <TestInfo info={info} />
        </Col>
        <Col span={15}>
          <ViewTable type="variant" data={variants} />
        </Col>
      </Row>
    </BasePage>
  );
};

export default OneTestPage;
