import { useNavigate } from "react-router-dom"; // Для навигации
import { Button, Flex, Form, Input, Space } from "antd";

export default function MainUnauthorizedPage() {
  const navigate = useNavigate();

  function clickRegisterButton() {
    console.log("Register Page");
    navigate("/register");
  }

  function onFinish(values) {
    console.log("Received values of form: ", values);
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
