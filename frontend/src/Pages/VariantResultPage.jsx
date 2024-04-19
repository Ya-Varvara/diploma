import React from "react";
import { useLocation } from "react-router-dom";
import FileViewer from "../Components/PDFViewer";

import {
  Card,
  Input,
  Space,
  List,
  Radio,
  Checkbox,
  Typography,
  Divider,
  Tag,
} from "antd";
import BasePage from "../Components/Layout/BasePage";
import GraphMatrix from "../Components/Forms/GraphMatrix";

const RenderForm = (props) => {
  switch (props.type.id) {
    case 1:
      return <GraphMatrix json={props.data} />;
    case 2:
      return <Input {...props} />;
    case 3:
      return (
        <Radio.Group {...props}>
          <Radio value={1}>Option 1</Radio>
          <Radio value={2}>Option 2</Radio>
          <Radio value={3}>Option 3</Radio>
        </Radio.Group>
      );
    case 4:
      return (
        <Checkbox.Group
          options={["Option 1", "Option 2", "Option 3"]}
          {...props}
        />
      );
    case 5:
      return <></>;
    case 6:
      return <TextArea rows={4} {...props} />;
    default:
      return null;
  }
};

const VariantResultInfo = ({ info }) => {
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
  if (!info) {
    return <></>;
  }
  return (
    <Card title="Информация о решении">
      <List>
        <List.Item>
          <Title level={5}>Имя Фамилия:</Title>
          <Text>
            {info.students_name} {info.students_surname}
          </Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Время начала:</Title>
          <Text>{formatDate(info.start_datetime)}</Text>
        </List.Item>
        <List.Item>
          <Title level={5}>Время окончания:</Title>
          <Text>{formatDate(info.end_datetime)}</Text>
        </List.Item>
      </List>
    </Card>
  );
};

const GraphAnswer = ({ data }) => {
  const { Title, Text } = Typography;
  const cutString = data.cut
    .map((pair) => `x${pair[0]} -> x${pair[1]}`)
    .join(", ");
  const reverseCutString = data.reverse_cut
    .map((pair) => `x${pair[0]} -> x${pair[1]}`)
    .join(", ");

  const subsetAString = data.cut_A.map((i) => `x${i}`).join(", ");
  const subsetBString = data.cut_B.map((i) => `x${i}`).join(", ");
  return (
    <List size="small">
      <List.Item>
        <Title level={5} type="secondary">
          Ребра разреза
        </Title>
        <Text type="secondary">{cutString}</Text>
      </List.Item>
      <List.Item>
        <Title level={5} type="secondary">
          Ребра обратного разреза
        </Title>
        <Text type="secondary">{reverseCutString}</Text>
      </List.Item>
      <List.Item>
        <Title level={5} type="secondary">
          Вершины в подмножестве А
        </Title>
        <Text type="secondary">{subsetAString}</Text>
      </List.Item>
      <List.Item>
        <Title level={5} type="secondary">
          Вершины в подмножестве B
        </Title>
        <Text type="secondary">{subsetBString}</Text>
      </List.Item>
      <List.Item>
        <Title level={5} type="secondary">
          Максимальный поток
        </Title>
        <Text type="secondary">{data.max_flow}</Text>
      </List.Item>
    </List>
  );
};

const StudentAnswer = ({ answer }) => {
  const { Title, Text } = Typography;
  return (
    <Tag
      color={answer.is_correct ? "green" : "red"}
      style={{ minWidth: "100%" }}
    >
      <List>
        <List.Item>
          <Title level={5}>Ответ:</Title>
          <Text>{answer.answer.int ? answer.answer.int : "Ответ не дан"}</Text>
        </List.Item>
      </List>
    </Tag>
  );
};

const VariantResultPage = () => {
  const location = useLocation();

  const variantData = location.state?.variantData;
  console.log(variantData);

  return (
    <BasePage>
      <Space direction="vertical" size="middle">
        <h1>{variantData.test_info.name}</h1>
        <VariantResultInfo info={variantData.variant_result_info} />
        <Space size="middle" direction="vertical">
          {variantData.tasks.map((task, index) => {
            return (
              <Card title={`Задание ${index + 1}`} style={{ minWidth: 800 }}>
                <Space size="middle" direction="vertical">
                  <div>{task.task.description_data}</div>
                  <div>
                    <RenderForm
                      type={task.task.type.condition_forms[0]}
                      data={task.task.condition_data}
                    />
                  </div>
                  <StudentAnswer answer={task.students_result} />
                  <Divider orientation="left">Правильный ответ</Divider>
                  <GraphAnswer data={task.task.answer_data} />
                </Space>
              </Card>
            );
          })}
        </Space>
        {variantData.uploaded_file ? (
          <FileViewer fileId={variantData.uploaded_file.id} />
        ) : (
          <></>
        )}
      </Space>
    </BasePage>
  );
};

export default VariantResultPage;
