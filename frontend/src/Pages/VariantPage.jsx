import React from "react";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom"; // Для навигации

import { Card, Form, Input, Space, Button, Radio, Checkbox } from "antd";
import BasePage from "../Components/Layout/BasePage";
import GraphMatrix from "../Components/Forms/GraphMatrix";

const { Item } = Form;

const RenderForm = (props) => {
  switch (props.type.id) {
    case 1:
      return <GraphMatrix json={props.data} />;
    case 2:
      return <Input {...props} />;
    case 3:
      return (
        <Radio.Group {...props}>
          <Radio value={1}>Option 1</Radio>
          <Radio value={2}>Option 2</Radio>
          <Radio value={3}>Option 3</Radio>
        </Radio.Group>
      );
    case 4:
      return (
        <Checkbox.Group
          options={["Option 1", "Option 2", "Option 3"]}
          {...props}
        />
      );
    case 5:
      return <></>;
    case 6:
      return <TextArea rows={4} {...props} />;
    default:
      return null;
  }
};

const VariantPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const testData = location.state?.testData;

  const [form] = Form.useForm();

  const [tasks, setTasks] = useState([]);

  const [remainingTime, setRemainingTime] = useState("");
  const [testStartTime, setTestStartTime] = useState(
    localStorage.getItem("testStartTime") || new Date().getTime()
  );

  const getSecondsFromTestTime = (testTime) => {
    const [hours, minutes, seconds] = testTime.split(":").map(Number);
    return hours * 3600 + minutes * 60 + seconds;
  };

  const submitFormWithTime = () => {
    const spentTime = CountSpentTime();
    // form.setFieldValue("spent_time", spentTime);
    form.setFieldsValue({ spentTime: spentTime });
    console.log(form);
    form.submit();
  };

  const CountSpentTime = () => {
    const now = new Date().getTime();
    const totalTime = Math.floor((now - parseInt(testStartTime, 10)) / 1000);
    const hours = Math.floor(totalTime / 3600);
    const minutes = Math.floor((totalTime % 3600) / 60);
    const seconds = totalTime % 60;
    const formattedTime = `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`;
    return formattedTime;
  };

  const updateTimer = () => {
    const now = new Date().getTime();
    const testDurationSeconds = getSecondsFromTestTime(testData.test_time);
    const endTime = parseInt(testStartTime, 10) + testDurationSeconds * 1000;
    const timeLeft = endTime - now;

    if (timeLeft < 0) {
      setRemainingTime("00:00:00");
      // Вычисляем общее затраченное время
      form.submit();
    } else {
      const hours = Math.floor((timeLeft / (1000 * 60 * 60)) % 24);
      const minutes = Math.floor((timeLeft / 1000 / 60) % 60);
      const seconds = Math.floor((timeLeft / 1000) % 60);
      setRemainingTime(
        `${hours.toString().padStart(2, "0")}:${minutes.toString().padStart(2, "0")}:${seconds.toString().padStart(2, "0")}`
      );
    }
  };

  useEffect(() => {
    let interval;

    if (testData) {
      updateTimer();
      interval = setInterval(updateTimer, 1000);
    }

    return () => clearInterval(interval);
  }, [testData, testStartTime]);

  useEffect(() => {
    if (location.state?.testData) {
      setTasks(location.state.testData.tasks);
    }
  }, [location.state]);

  if (!testData) {
    return <div>No test data available</div>;
  }

  const onFinish = (values) => {
    const spentTime = CountSpentTime();
    console.log("Spent time", spentTime);
    console.log("Received values of variant: ", values);
    localStorage.removeItem("testStartTime");
    navigate("/home");
  };

  return (
    <BasePage>
      <Space direction="vertical" size="middle">
        <h1>{testData.name}</h1>
        {/* Отображение таймера */}
        <h2>Оставшееся время: {remainingTime}</h2>
        {/* Остальная часть формы */}
        <Form
          form={form}
          name="create_task_type"
          onFinish={onFinish}
          layout="vertical"
          style={{ maxWidth: 800 }}
        >
          <Item
            label="Имя"
            name="name"
            rules={[{ required: true, message: "Введите имя" }]}
          >
            <Input />
          </Item>
          <Item
            label="Фамилия"
            name="surname"
            rules={[{ required: true, message: "Введите фамилию" }]}
          >
            <Input />
          </Item>
          <Space size="middle" direction="vertical">
            {tasks.map((task, index) => {
              return (
                <Card title={`Задание ${index + 1}`} style={{ minWidth: 800 }}>
                  <Space size="middle" direction="vertical">
                    <Item name={`desc_${index + 1}`} label="Описание">
                      {task.description_data}
                    </Item>
                    <Item name={`cond_${index + 1}`} label="Условие">
                      <RenderForm
                        type={task.type.condition_forms[0]}
                        data={task.condition_data}
                      />
                    </Item>
                    <Item name={`answer_${index + 1}`} label="Ответ">
                      <RenderForm type={task.type.answer_forms[0]} data={""} />
                    </Item>
                  </Space>
                </Card>
              );
            })}
            <Form.Item>
              <Button type="primary" htmlType="submit">
                Отправить
              </Button>
            </Form.Item>
          </Space>
        </Form>
      </Space>
    </BasePage>
  );
};

export default VariantPage;
