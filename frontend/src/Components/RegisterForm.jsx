import React from "react";
import { useNavigate } from "react-router-dom"; // Для навигации
import { Button, Form, Input, Flex } from "antd";
import { useAuth } from "../AuthContext";
// import "./RegisterForm.css";

const formItemLayout = {
  labelCol: {
    xs: {
      span: 24,
    },
    sm: {
      span: 8,
    },
  },
  wrapperCol: {
    xs: {
      span: 24,
    },
    sm: {
      span: 16,
    },
  },
};
const tailFormItemLayout = {
  wrapperCol: {
    xs: {
      span: 24,
      offset: 0,
    },
    sm: {
      span: 16,
      offset: 8,
    },
  },
};

export default function RegisterForm() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [form] = Form.useForm();

  function onFinish(values) {
    console.log("Received values of form: ", values);

    const requestBody = {
      email: values.email,
      password: values.password,
      username: values.username, // Используем значение nickname как username
      is_active: true,
      is_superuser: false,
      is_verified: false,
      id: 1000
    };

    fetch('http://localhost:8000/auth/register', {
      method: 'POST', // Метод запроса
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include', // Указываем, что мы хотим использовать cookies
      body: JSON.stringify(requestBody),
    })
    .then(response => {
      if (response.status === 201) {
        console.log("Login successful");
        // login(); // Предположим, что это функция для установки состояния аутентификации
        navigate("/login"); // Переход на главную страницу или другую страницу после успешного входа
      } else if (!response.ok) {
        throw new Error('Login failed with status: ' + response.status);
      }
    })
    .catch(error => {
      console.error(error.message);
      // Здесь можно обработать ошибку, например, показать пользователю сообщение
    });
  }

  return (
    <Form
      {...formItemLayout}
      form={form}
      name="register"
      onFinish={onFinish}
      style={{
        maxWidth: 600,
        minWidth: 500,
      }}
      scrollToFirstError
    >
      <Form.Item
        name="email"
        label="E-mail"
        rules={[
          {
            type: "email",
            message: "The input is not valid E-mail!",
          },
          {
            required: true,
            message: "Please input your E-mail!",
          },
        ]}
      >
        <Input />
      </Form.Item>

      <Form.Item
        name="password"
        label="Password"
        rules={[
          {
            required: true,
            message: "Please input your password!",
          },
        ]}
        hasFeedback
      >
        <Input.Password />
      </Form.Item>

      <Form.Item
        name="confirm"
        label="Confirm Password"
        dependencies={["password"]}
        hasFeedback
        rules={[
          {
            required: true,
            message: "Please confirm your password!",
          },
          ({ getFieldValue }) => ({
            validator(_, value) {
              if (!value || getFieldValue("password") === value) {
                return Promise.resolve();
              }
              return Promise.reject(
                new Error("The new password that you entered do not match!")
              );
            },
          }),
        ]}
      >
        <Input.Password />
      </Form.Item>

      <Form.Item
        name="username"
        label="Username"
        tooltip="What do you want others to call you?"
        rules={[
          {
            required: true,
            message: "Please input your username!",
            whitespace: true,
          },
        ]}
      >
        <Input />
      </Form.Item>
      <Form.Item {...tailFormItemLayout}>
        <Button type="primary" htmlType="submit">
          Register
        </Button>
      </Form.Item>
    </Form>
  );
}
