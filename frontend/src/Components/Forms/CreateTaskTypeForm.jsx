import React, { useState, useEffect } from "react";
import {
  Form,
  Input,
  Button,
  Select,
  Radio,
  Checkbox,
  Upload,
  message,
  Card,
  Space,
} from "antd";
import { UploadOutlined } from "@ant-design/icons"; // Если вы используете иконку загрузки
import "./CreateTaskTypeForm.css";
import GraphMatrix from "./GraphMatrix";
import data from "./data.json";

const { Option } = Select;

export default function CreateTaskTypeForm() {
  const [form] = Form.useForm();
  const [baseTypes, setBaseTypes] = useState([]);
  const [forms, setForms] = useState([]);
  const [selectedBaseType, setSelectedBaseType] = useState();
  const [selectedConditionForm, setSelectedConditionForm] = useState([]);
  const [selectedAnswerForm, setSelectedAnswerForm] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/task_type/base_types/", {
      credentials: "include", // Для отправки и приёма куки
    })
      .then((response) => response.json())
      .then((data) => {
        setBaseTypes(data);
        console.log(data);
      })
      .catch((error) => {
        message.error("Ошибка при загрузке базовых типов заданий");
      });

    fetch("http://localhost:8000/forms/", {
      credentials: "include", // Для отправки и приёма куки
    })
      .then((response) => response.json())
      .then((data) => {
        setForms(data);
        console.log(data);
      })
      .catch((error) => {
        message.error("Ошибка при загрузке форм интерфейсов");
      });
  }, []);
  const onFinish = (values) => {
    console.log("Received values of form: ", values);
    // Здесь можно добавить логику отправки данных формы на сервер
    const requestBody = {
      name: values.name,
      condition_forms: values.condition_forms_ids, // Если формы не выбраны, используем массив с 0
      answer_forms: values.answer_forms_ids, // Аналогично для форм ответа
    };

    // Добавление базового типа и настроек, если базовый тип выбран
    if (values.base_task_type_id) {
      const settings = {};
      Object.keys(values.settings).forEach((key) => {
        settings[key] = values.settings[key];
      });
      requestBody.settings = settings;
      requestBody.base_task_type = values.base_task_type_id;
    }

    fetch("http://localhost:8000/task_type/", {
      method: "POST", // Метод запроса
      headers: {
        "Content-Type": "application/json",
      },
      credentials: "include", // Указываем, что мы хотим использовать cookies
      body: JSON.stringify(requestBody),
    })
      .then((response) => {
        if (response.status === 201) {
          console.log("Task Type was created successfully");
        } else if (!response.ok) {
          throw new Error(
            "Task Type creation failed with status: " + response.status
          );
        }
      })
      .catch((error) => {
        console.error(error.message);
        // Здесь можно обработать ошибку, например, показать пользователю сообщение
      });
  };

  // Обработчик изменения выбранного базового типа
  const onBaseTypeChange = (value) => {
    setSelectedBaseType(baseTypes.find((type) => type.id === value));
  };

  const onConditionFormChange = (values) => {
    // Преобразование каждого ID из values в соответствующий объект формы
    const selectedForms = values.map((value) =>
      forms.find((form) => form.id === value)
    );

    // Установка массива выбранных форм в состояние
    setSelectedConditionForm(selectedForms);

    // Для проверки, можно вывести в консоль выбранные формы
    console.log("Selected Condition Forms: ", selectedForms);
  };

  const onAnswerFormChange = (values) => {
    // Преобразование каждого ID из values в соответствующий объект формы
    const selectedForms = values.map((value) =>
      forms.find((form) => form.id === value)
    );
    // Установка массива выбранных форм в состояние
    setSelectedAnswerForm(selectedForms);
    // Для проверки, можно вывести в консоль выбранные формы
    console.log("Selected Answer Forms: ", selectedForms);
  };

  // Функция для генерации дополнительных полей ввода
  const generateAdditionalFields = () => {
    if (!selectedBaseType || !selectedBaseType.settings) return null;

    return Object.entries(selectedBaseType.settings).map(
      ([key, type], index) => (
        <Form.Item
          key={index}
          name={["settings", key]}
          label={key}
          rules={[{ required: true, message: `Пожалуйста, введите ${key}!` }]}
        >
          <Input type={type === "int" ? "number" : "text"} />
        </Form.Item>
      )
    );
  };

  const renderField = (type) => {
    switch (type) {
      case "table":
        return <GraphMatrix json={data} />;
      case "input":
        return <Input key={type} />;
      case "radio":
        return (
          <Radio.Group key={type}>
            <Radio value={1}>Опция 1</Radio>
            <Radio value={2}>Опция 2</Radio>
            <Radio value={3}>Опция 3</Radio>
          </Radio.Group>
        );
      case "checkbox":
        return (
          <Checkbox.Group
            key={type}
            options={["Опция 1", "Опция 2", "Опция 3"]}
          />
        );
      case "upload":
        return (
          <Upload key={type}>
            <Button icon={<UploadOutlined />}>Загрузить файл</Button>
          </Upload>
        );
      case "text":
        return <Input.TextArea key={type} />;
      default:
        return null;
    }
  };

  const conditionForms = Array.isArray(forms)
    ? forms.filter((form) => form.condition_form)
    : null;

  const answerForms = Array.isArray(forms)
    ? forms.filter((form) => form.answer_form)
    : null;

  return (
    <div>
      <Form
        form={form}
        name="create_task_type"
        onFinish={onFinish}
        layout="vertical"
        style={{ maxWidth: 800 }}
      >
        <Form.Item
          name="name"
          label="Название типа"
          rules={[
            { required: true, message: "Пожалуйста, введите название типа!" },
          ]}
        >
          <Input />
        </Form.Item>

        <Form.Item name="base_task_type_id" label="Базовый тип">
          <Select allowClear onChange={onBaseTypeChange}>
            {baseTypes.map((type) => (
              <Option key={type.id} value={type.id}>
                {type.name}
              </Option>
            ))}
          </Select>
        </Form.Item>

        {/* Динамически добавляемые поля на основе выбранного базового типа */}
        {generateAdditionalFields()}

        <Form.Item
          name="condition_forms_ids"
          label="Форма интерфейса представления задания"
          rules={[
            {
              required: true,
              message: "Выберите форму интерфейса представления задания!",
            },
          ]}
        >
          <Select mode="multiple" allowClear onChange={onConditionFormChange}>
            {conditionForms.map((form) => (
              <Option key={form.id} value={form.id}>
                {form.name}
              </Option>
            ))}
            {/* {conditionForms} */}
          </Select>
        </Form.Item>

        <Form.Item
          name="answer_forms_ids"
          label="Форма интерфейса ответа на задание"
          rules={[
            {
              required: true,
              message: "Выберите форму интерфейса ответа на задание!",
            },
          ]}
        >
          <Select mode="multiple" allowClear onChange={onAnswerFormChange}>
            {answerForms.map((form) => (
              <Option key={form.id} value={form.id}>
                {form.name}
              </Option>
            ))}
            {/* {answerForms} */}
          </Select>
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit">
            Создать тип задания
          </Button>
        </Form.Item>
      </Form>
      <Space direction="vertical" size="middle" style={{ display: "flex" }}>
        <Card title="Форма интерфейса представления задания" size="small">
          <p style={{ fontWeight: "bold" }}>Задание</p>
          <p style={{ fontWeight: "bold" }}>Описание задания:</p>
          <p>Сделать задание :/</p>
          <p style={{ fontWeight: "bold" }}>Условие</p>
          <div style={{ marginTop: "20px" }}>
            {selectedConditionForm &&
              Array.isArray(selectedConditionForm) &&
              selectedConditionForm.map((form) => renderField(form.short_name))}
          </div>
          <p style={{ fontWeight: "bold" }}>Ответ</p>
          <div style={{ marginTop: "20px" }}>
            {selectedAnswerForm &&
              Array.isArray(selectedAnswerForm) &&
              selectedAnswerForm.map((form) => renderField(form.short_name))}
          </div>
        </Card>
      </Space>
    </div>
  );
}
