import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Button, Flex, Form, Input, Modal, Space } from "antd";
import moment from "moment";

import { FetchTestVariantByLink, MakeTestVariantGiven } from "../Handlers/API";

export default function MainUnauthorizedPage() {
  const navigate = useNavigate();
  const [isModalVisible, setIsModalVisible] = useState(false);
  const [variant, setVariant] = useState("");
  const [testInfo, settestInfo] = useState("");
  const [form] = Form.useForm();

  const [isButtonDisabled, setIsButtonDisabled] = useState(true); // Добавляем состояние для отключения кнопки

  const formattedStartDatetime = moment(testInfo.start_datetime);
  const formattedEndDatetime = moment(testInfo.end_datetime);
  const currentTime = moment();

  useEffect(() => {
    if (
      currentTime.isAfter(formattedStartDatetime) &&
      currentTime.isBefore(formattedEndDatetime)
    ) {
      setIsButtonDisabled(false); // Кнопка доступна
    } else {
      setIsButtonDisabled(true); // Кнопка не доступна
    }
  }, [formattedStartDatetime, formattedEndDatetime, currentTime]);

  function clickRegisterButton() {
    navigate("/register");
  }

  async function onFinish(values) {
    try {
      const data = await FetchTestVariantByLink({ link: values.uuid });
      setVariant(data);
      settestInfo(data.test_info);
      console.log(variant);
      showModal();
    } catch (error) {
      console.error("Error fetching test variant:", error);
    }
  }

  function showModal() {
    setIsModalVisible(true);
  }

  function handleOk(values) {
    console.log(variant.id);
    form.submit();
    localStorage.setItem("variant", variant.id);
    MakeTestVariantGiven({ id: variant.id });
    navigate("/variant", { state: { testData: variant } });
    setIsModalVisible(false);
  }

  function handleCancel() {
    setIsModalVisible(false);
  }

  const onFinishModal = async (values) => {
    localStorage.setItem("name", values.name);
    localStorage.setItem("surname", values.surname);
  };

  return (
    <>
      <Space direction="vertical" size="small">
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
      </Space>
      <Modal
        title={`Тест: ${testInfo.name}`}
        open={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        okText="Да"
        cancelText="Нет"
        okButtonProps={{ disabled: isButtonDisabled }} // Устанавливаем свойство disabled
      >
        <p>
          Дата и время начала:{" "}
          {formattedStartDatetime.format("DD.MM.YYYY HH:mm")}
        </p>
        <p>
          Дата и время окончания:{" "}
          {formattedEndDatetime.format("DD.MM.YYYY HH:mm")}
        </p>
        <p>Продолжительность теста: {testInfo.test_time}</p>
        <p />
        <p>Вы готовы начать тестирование?</p>
        {!isButtonDisabled ? (
          <Form onFinish={onFinishModal} form={form}>
            <Form.Item
              key={"name"}
              name="name"
              rules={[{ required: true, message: "Введите ваше имя!" }]}
            >
              <Input placeholder="Имя" />
            </Form.Item>
            <Form.Item
              key={"surname"}
              name="surname"
              rules={[{ required: true, message: "Введите вашу фамилию!" }]}
            >
              <Input placeholder="Фамилия" />
            </Form.Item>
          </Form>
        ) : (
          <></>
        )}
      </Modal>
    </>
  );
}
