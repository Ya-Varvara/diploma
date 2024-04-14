import { useNavigate } from "react-router-dom"; // Для навигации
import { Button, Flex, Form, Input, Space } from "antd";

import React from "react";
import { useState, useEffect } from "react";

import { FetchTestVariantByLink } from "../Handlers/API";

export default function MainUnauthorizedPage() {
  const navigate = useNavigate();

  const [variant, setVariant] = useState({});

  // useEffect(() => {
  //   FetchTestByLink({ setter: setVariant, link: values.uuid });
  // }, []);

  function clickRegisterButton() {
    console.log("Register Page");
    navigate("/register");
  }

  async function onFinish(values) {
    console.log("Received values of form: ", values);
    try {
      const data = await FetchTestVariantByLink({ link: values.uuid });
      navigate("/variant", { state: { testData: data } });
    } catch (error) {
      console.error("Error fetching test variant:", error);
      // Можно обработать ошибку здесь, если необходимо
    }
  }

  return (
    <>
      <Flex gap="small" align="center" justify="center">
        <Flex gap="small" align="center" justify="center" vertical={true}>
          <Form onFinish={onFinish} layout="inline">
            <Form.Item
              name="uuid"
              rules={[
                { required: true, message: "Please input your uuid" },
                () => ({
                  validator(rule, value, callback) {
                    if (!value.trim()) {
                      return Promise.resolve();
                    }
                    if (value.length !== 36) {
                      return Promise.reject("Enter a valid uuid!");
                    }
                    if (!/^[a-zA-Z0-9-]+$/.test(value)) {
                      return Promise.reject("Enter a valid uuid!");
                    }
                    return Promise.resolve();
                  },
                }),
              ]}
            >
              <Input
                count={{
                  show: true,
                  max: 36,
                }}
                style={{ minWidth: "400px" }}
              />
            </Form.Item>
            <Form.Item>
              <Button htmlType="submit" type="primary">
                Перейти
              </Button>
            </Form.Item>
          </Form>
        </Flex>
        <Button type="link" onClick={clickRegisterButton}>
          Регистрация
        </Button>
      </Flex>
    </>
  );
}
