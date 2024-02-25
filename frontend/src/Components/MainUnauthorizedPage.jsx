import { useNavigate } from "react-router-dom"; // Для навигации
import { Button, Flex, Form } from "antd";

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
    <Flex vertical gap="large" style={{ maxWidth: "600px" }}>
      <Flex gap="small">
        {/* <Form>
          <Form.Item name="uuid"></Form.Item>
        </Form> */}
        <Button onClick={validateIdentifier}>Перейти</Button>
      </Flex>
      <Button type="link" onClick={clickRegisterButton}>
        Регистрация
      </Button>
    </Flex>
  );
}
