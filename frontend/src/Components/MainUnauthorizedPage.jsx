import { useNavigate } from "react-router-dom"; // Для навигации
import { Button, Flex, Form, Input } from "antd";

export default function MainUnauthorizedPage() {
  const navigate = useNavigate();

  function clickRegisterButton() {
    console.log("Register Page");
    navigate("/register");
  }

  function onFinish(values) {
    console.log("Received values of form: ", values);
  }

  function validateIdentifier(value) {
    const regex = /^[a-zA-Z0-9-]+$/;
    return regex.test(value) && value.trim() !== "";
  }

  return (
    <Flex vertical gap="large" style={{ maxWidth: "700px" }}>
      <Flex gap="small">
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
                //   if (value.length !== 36) {
                //     return Promise.reject("Enter a valid uuid!");
                //   }
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
              style={{minWidth: "500px"}}
            />
          </Form.Item>
          <Form.Item>
            <Button htmlType="submit">Перейти</Button>
          </Form.Item>
        </Form>
      </Flex>
      <Button type="link" onClick={clickRegisterButton}>
        Регистрация
      </Button>
    </Flex>
  );
}
