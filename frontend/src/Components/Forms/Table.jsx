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
  console.log(data);
  const navigate = useNavigate();

  const findVariantById = ({ id }) => {
    // Используем метод find для поиска первого объекта с указанным id.
    console.log(id);
    const result = data.find((item) => item.id === id);
    console.log(result);
    return result; // Возвращаем найденный объект или null, если ничего не найдено.
  };

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

  const variant_columns = [
    {
      title: "Вариант",
      dataIndex: "variant",
      key: "variant",
    },
    {
      title: "Статус",
      key: "status",
      render: (_, record) => {
        if (record.is_given) {
          if (record.variant_result_info) {
            return (
              <Tag color={"green"} key={1}>
                Ответ отправлен
              </Tag>
            );
          } else {
            return (
              <Tag color={"orange"} key={2}>
                Выдан
              </Tag>
            );
          }
        } else {
          return (
            <Tag color={"red"} key={2}>
              Не выдан
            </Tag>
          );
        }
      },
    },
    {
      title: "ФИО",
      key: "fullName",
      render: (_, record) => {
        if (record.is_given && record.variant_result_info) {
          return `${record.variant_result_info.students_surname} ${record.variant_result_info.students_name}`;
        }
        return "";
      },
    },
    {
      title: "Дата отправки",
      key: "end_datetime",
      render: (_, record) => {
        if (
          record.is_given &&
          record.variant_result_info &&
          record.variant_result_info.end_datetime
        ) {
          // Преобразуем дату в более читаемый формат, например "DD.MM.YYYY HH:mm"
          return new Date(
            record.variant_result_info.end_datetime
          ).toLocaleString("ru-RU", {
            year: "numeric",
            month: "numeric",
            day: "numeric",
            hour: "2-digit",
            minute: "2-digit",
          });
        }
        return ""; // Возвращаем пустую строку, если статус не "Ответ отправлен"
      },
    },
    {
      title: "Действия",
      key: "actions",
      render: (text, record, index) => {
        return (
          <Button
            type="link"
            onClick={() =>
              navigate(
                `/home/tests/${record.test_info.test_id}/variant/${record.id}`,
                {
                  state: { variantData: findVariantById({ id: record.id }) },
                }
              )
            }
          >
            Перейти
          </Button>
        );
      },
    },
  ];

  if (type === "test") {
    return <Table columns={test_columns} dataSource={data} bordered />;
  } else if (type === "task_type") {
    return <Table columns={task_type_columns} dataSource={data} bordered />;
  } else if (type === "variant") {
    return <Table columns={variant_columns} dataSource={data} bordered />;
  }
};

export default ViewTable;
