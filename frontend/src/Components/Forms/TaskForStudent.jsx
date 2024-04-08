import React from "react";
import { useState } from "react";

import GraphMatrix from "./GraphMatrix";

import {
  Card,
  Form,
  Input,
  Radio,
  Checkbox,
  Upload,
  Button,
  Space,
} from "antd";
import { UploadOutlined } from "@ant-design/icons";

function renderForm({ type, data }) {
  console.log("Render form data:", type, data);
  switch (type.id) {
    case 1:
      return <GraphMatrix json={data} />;
    case 2:
      return <Input />;
    case 3:
      return (
        <Radio.Group>
          <Radio value={1}>Option 1</Radio>
          <Radio value={2}>Option 2</Radio>
          <Radio value={3}>Option 3</Radio>
        </Radio.Group>
      );
    case 4:
      return <Checkbox.Group options={["Option 1", "Option 2", "Option 3"]} />;
    case 5:
      return (
        <Upload>
          <Button icon={<UploadOutlined />}>Upload Files</Button>
        </Upload>
      );
    case 6:
      return <TextArea rows={4} />;
    default:
      return null;
  }
}

export default function TaskForStudent({ task_info, number, form }) {
  console.log("In Task For Student:", task_info, number, form);

  const onFinish = (values) => {
    console.log("Received values of variant: ", values);
  };

  return (
    // <Card title={`Задание ${number}`}>
      <Space size="middle" direction="vertical">
        <p>
          <strong>Описание:</strong> {task_info.description_data}
        </p>
        <p>
          <strong>Условие:</strong>
          {renderForm({
            type: task_info.type.condition_forms[0],
            data: task_info.condition_data,
          })}
        </p>
        <Form layout="vertical" onFinish={onFinish}>
          <Form.Item>
            {renderForm({ type: task_info.type.answer_forms[0], data: "" })}
          </Form.Item>
        </Form>
      </Space>
    // </Card>
  );
}
