import React from "react";
import { useNavigate } from "react-router-dom"; // Для навигации
import { LockOutlined, MailOutlined, EyeTwoTone } from "@ant-design/icons";
import { Button, Checkbox, Form, Input, Flex } from "antd";
import { useAuth } from "../../AuthContext";
import "./LogInForm.css";

export default function LogInForm() {
  const navigate = useNavigate();
  const { login } = useAuth();

  function onFinish(values) {
    console.log("Received values of form: ", values);
    login();
    navigate("/");
  }

  function onFinishFailed(errorInfo) {
    console.log("Failed:", errorInfo);
  }

  function clickRegisterButton() {
    console.log("Register Page");
    navigate("/register");
  }

  return (
    <Flex align="center" justify="center">
      <Form
        name="normal_login"
        className="login-form"
        initialValues={{
          remember: false,
        }}
        onFinish={onFinish}
        onFinishFailed={onFinishFailed}
        // autoComplete="off"
      >
        <Form.Item
          name="email"
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
          <Input
            prefix={<MailOutlined className="site-form-item-icon" />}
            placeholder="E-mail"
          />
        </Form.Item>
        <Form.Item
          name="password"
          rules={[
            {
              required: true,
              message: "Please input your Password!",
            },
          ]}
        >
          <Input.Password
            prefix={<LockOutlined className="site-form-item-icon" />}
            type="password"
            placeholder="Password"
          />
        </Form.Item>
        <Form.Item>
          <Form.Item name="remember" valuePropName="checked" noStyle>
            <Checkbox>Remember me</Checkbox>
          </Form.Item>

          <a className="login-form-forgot" href="">
            Forgot password
          </a>
        </Form.Item>

        <Form.Item>
          <Button
            type="primary"
            htmlType="submit"
            className="login-form-button"
          >
            Log in
          </Button>
          Or
          <Button type="link" onClick={clickRegisterButton}>
            register now!
          </Button>
        </Form.Item>
      </Form>
    </Flex>
  );
}
