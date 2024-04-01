import React from "react";
import { Space, Table, Tag } from "antd";

const test_columns = [
  {
    title: "Номер",
    dataIndex: "id",
    key: "id",
  },
  {
    title: "Название",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "Кол-во вариантов",
    dataIndex: "variants_number",
    key: "variants_number",
  },
  {
    title: "Дата начала",
    dataIndex: "start_datetime",
    key: "start_datetime",
  },
  {
    title: "Дата окончания",
    dataIndex: "end_datetime",
    key: "end_datetime",
  },
  {
    title: "Ссылка",
    dataIndex: "link",
    key: "link",
  },
  {
    title: "Действия",
    key: "action",
    render: (_, record) => (
      <Space size="middle">
        <a>Посмотреть</a>
        <a>Удалить</a>
      </Space>
    ),
  },
];

const task_type_columns = [
  {
    title: "Номер",
    dataIndex: "id",
    key: "id",
  },
  {
    title: "Название",
    dataIndex: "name",
    key: "name",
  },
  {
    title: "Действия",
    key: "action",
    render: (_, record) => (
      <Space size="middle">
        <a>Посмотреть</a>
        <a>Удалить</a>
      </Space>
    ),
  },
];

const ViewTable = ({ type, data }) => {
  if (type === "test") {
    return <Table columns={test_columns} dataSource={data} bordered />;
  } else if (type === "task_type") {
    return <Table columns={task_type_columns} dataSource={data} bordered />;
  }
};

export default ViewTable;
