import React, { useState, useEffect } from "react";
import {
  Form,
  Input,
  DatePicker,
  TimePicker,
  InputNumber,
  Button,
  Select,
  message,
  Card,
} from "antd";
import { CloseOutlined } from "@ant-design/icons";

const { RangePicker } = DatePicker;

const CreateTestForm = () => {
  // Формат для времени выполнения
  const timeFormat = "HH:mm";
  const dateFormat = "YYYY-MM-DD HH:mm";

  const [taskTypes, setTaskTypes] = useState([]); // Состояние для хранения типов заданий
  const [form] = Form.useForm();

  useEffect(() => {
    fetch("http://localhost:8000/task_type/", {
      credentials: "include", // Для отправки и приёма куки
    })
      .then((response) => response.json())
      .then((data) => {
        setTaskTypes(data);
        console.log(data);
      })
      .catch((error) => {
        message.error("Ошибка при загрузке типов заданий");
      });
  }, []);

  // Обработчик отправки формы
  const onFinish = (values) => {
    console.log("Received values of form: ", values);
  };

  return (
    <Form
      onFinish={onFinish}
      //   layout="vertical"
      form={form}
      autoComplete="off"
      labelCol={{ span: 10 }}
      wrapperCol={{ span: 18 }}
      style={{ maxWidth: 800 }}
    >
      <Form.Item
        name="name"
        label="Название тестирования"
        rules={[
          {
            required: true,
            message: "Пожалуйста, введите название тестирования!",
          },
        ]}
      >
        <Input placeholder="Введите название" />
      </Form.Item>

      <Form.Item
        name="dates"
        label="Начало и конец"
        rules={[
          { required: true, message: "Пожалуйста, выберите начало и конец!" },
        ]}
      >
        <RangePicker showTime format={dateFormat} />
      </Form.Item>

      <Form.Item
        name="test_time"
        label="Время выполнения"
        rules={[
          { required: true, message: "Пожалуйста, выберите время выполнения!" },
        ]}
      >
        <TimePicker format={timeFormat} />
      </Form.Item>

      <Form.Item
        name="variants"
        label="Количество вариантов"
        rules={[
          {
            required: true,
            message: "Пожалуйста, выберите количество вариантов!",
          },
        ]}
      >
        <InputNumber min={1} step={1} />
      </Form.Item>

      <Form.List name="tasks">
        {(fields, { add, remove }) => (
          <div
            style={{
              display: "flex",
              rowGap: 16,
              flexDirection: "column",
            }}
          >
            {fields.map(({ key, name, fieldKey, ...restField }) => (
              <Card
                size="small"
                title={`Задание ${key + 1}`}
                key={key}
                extra={
                  <CloseOutlined
                    onClick={() => {
                      remove(name);
                    }}
                  />
                }
              >
                <Form.Item
                  {...restField}
                  name={[name, "type"]}
                  label="Тип задания"
                  fieldKey={[fieldKey, "type"]}
                  rules={[
                    {
                      required: true,
                      message: "Пожалуйста, выберите тип задания!",
                    },
                  ]}
                >
                  <Select
                    placeholder="Выберите тип задания"
                    // style={{ width: 200 }}
                  >
                    {taskTypes.map((task) => (
                      <Option key={task.id} value={task.id}>
                        {task.name}
                      </Option>
                    ))}
                  </Select>
                </Form.Item>
                <Form.Item
                  {...restField}
                  label="Количество заданий"
                  name={[name, "quantity"]}
                  fieldKey={[fieldKey, "quantity"]}
                  rules={[
                    {
                      required: true,
                      message: "Пожалуйста, введите количество заданий!",
                    },
                  ]}
                >
                  <InputNumber min={1} placeholder="Количество" />
                </Form.Item>
                {/* <Button type="danger" onClick={() => remove(name)}>
                  Удалить
                </Button> */}
              </Card>
            ))}
            <Button type="dashed" onClick={() => add()} block icon="+">
              Добавить задание
            </Button>
          </div>
        )}
      </Form.List>

      <Form.Item>
        <Button type="primary" htmlType="submit">
          Создать
        </Button>
      </Form.Item>
    </Form>
  );
};

export default CreateTestForm;
