import React from "react";
import { useNavigate } from "react-router-dom";
import { Space, Table, Tag, Button } from "antd";
import { Typography } from "antd";

import { DeleteTaskTypeByID, DeleteTestByID } from "../../Handlers/API";

const { Paragraph, Text } = Typography;

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
        {/* <a>Посмотреть</a> */}
        <Button
          type="link"
          onClick={() => DeleteTaskTypeByID({ id: record.id })}
        >
          Удалить
        </Button>
      </Space>
    ),
  },
];

const ViewTable = ({ type, data }) => {
  const navigate = useNavigate();

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
      key: "link",
      render: (_, record) => <Paragraph copyable>{record.link}</Paragraph>,
    },
    {
      title: "Действия",
      key: "action",
      render: (_, record) => (
        <Space size="small">
          <Button
            type="link"
            onClick={() => navigate(`/home/tests/${record.id}`)}
          >
            Перейти
          </Button>
          <Button type="link" onClick={() => DeleteTestByID({ id: record.id })}>
            Удалить
          </Button>
        </Space>
      ),
    },
  ];

  if (type === "test") {
    return <Table columns={test_columns} dataSource={data} bordered />;
  } else if (type === "task_type") {
    return <Table columns={task_type_columns} dataSource={data} bordered />;
  }
};

export default ViewTable;
