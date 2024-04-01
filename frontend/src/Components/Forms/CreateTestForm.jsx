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
  Drawer,
  Space,
} from "antd";
import { CloseOutlined } from "@ant-design/icons";
import { UploadOutlined } from "@ant-design/icons"; // Если вы используете иконку загрузки

const { RangePicker } = DatePicker;

const CreateTestForm = ({ open, onClose }) => {
  const timeFormat = "HH:mm";
  const dateFormat = "YYYY-MM-DD HH:mm";

  const [form] = Form.useForm();

  const [taskTypes, setTaskTypes] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/task_type/", {
      credentials: "include",
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

  const onFinish = (values) => {
    console.log("Received values of form: ", values);

    const start_datetime = values.dates[0].toISOString();
    const end_datetime = values.dates[1].toISOString();
    const test_time = values.test_time.format("HH:mm:ss.SSS") + "Z";

    console.log("datetime: ", start_datetime, end_datetime, test_time);

    const task_types = values.tasks.map((task) => ({
      type_id: task.type,
      number: task.quantity,
    }));

    const requestData = {
      name: values.name,
      start_datetime: start_datetime,
      end_datetime: end_datetime,
      test_time: test_time,
      variants_number: values.variants,
      task_types: task_types,
    };

    fetch("http://localhost:8000/test/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include",
      body: JSON.stringify(requestData),
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Ошибка при отправке данных");
      })
      .then((data) => {
        console.log("Успешно:", data);
        message.success("Тест успешно создан");
      })
      .catch((error) => {
        console.error("Ошибка:", error);
        message.error("Ошибка при создании теста");
      });

    form.resetFields();
    onClose();
  };

  return (
    <Drawer
      title="Создание теста"
      width={900}
      onClose={onClose}
      open={open}
      styles={{
        body: {
          paddingBottom: 80,
        },
      }}
      extra={
        <Space>
          <Button
            htmlType="submit"
            onClick={() => form.submit()}
            type="primary"
          >
            Создать
          </Button>
        </Space>
      }
    >
      <Form
        onFinish={onFinish}
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
            {
              required: true,
              message: "Пожалуйста, выберите время выполнения!",
            },
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
      </Form>
    </Drawer>
  );
};

export default CreateTestForm;
