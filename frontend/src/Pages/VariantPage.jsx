import React from "react";
import { useEffect, useState } from "react";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom"; // Для навигации

import {
  Card,
  Form,
  Input,
  Space,
  Button,
  Radio,
  Checkbox,
  Upload,
  Modal,
} from "antd";
import BasePage from "../Components/Layout/BasePage";
import GraphMatrix from "../Components/Forms/GraphMatrix";
import { PostVariantResult, sendFileToServer, baseURL } from "../Handlers/API";

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

  const [testData, setTestData] = useState();
  // console.log(testData);

  useEffect(() => {
    async function FetchTestVariantByID({ id }) {
      try {
        const response = await fetch(`${baseURL}/variant/id/?id=${id}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
        });
        if (!response.ok) {
          throw new Error("Test variant fetching failed: " + response.status);
        }
        const data = await response.json();
        console.log("In Fetch Test By ID: ", data);
        setTestData(data);
        setTasks(data.tasks);
      } catch (error) {
        console.error(error);
      }
    }
    FetchTestVariantByID({ id: parseInt(localStorage.getItem("variant")) });
    console.log(testData);
  }, []);

  const [form] = Form.useForm();
  const [isModalVisible, setIsModalVisible] = useState(false);

  const [tasks, setTasks] = useState([]);
  const [file, setFile] = useState();
  // console.log(file);

  const [remainingTime, setRemainingTime] = useState("");
  const [testStartTime, setTestStartTime] = useState(
    localStorage.getItem("testStartTime") || new Date().getTime()
  );
  const [testStartDateTime, setTestStartDateTime] = useState(
    localStorage.getItem("testStartDateTime") || new Date()
  );

  const getSecondsFromTestTime = (testTime) => {
    const [hours, minutes, seconds] = testTime.split(":").map(Number);
    return hours * 3600 + minutes * 60 + seconds;
  };

  const showModal = () => {
    setIsModalVisible(true);
  };

  const handleOk = async () => {
    setIsModalVisible(false);
    form.submit();
  };

  const handleCancel = () => {
    setIsModalVisible(false);
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
    const testDurationSeconds = getSecondsFromTestTime(
      testData.test_info.test_time
    );
    const endTime = parseInt(testStartTime, 10) + testDurationSeconds * 1000;
    const timeLeft = endTime - now;

    if (timeLeft < 0) {
      setRemainingTime("00:00:00");
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
      const startTime = localStorage.getItem("testStartTime");
      const startDateTime = localStorage.getItem("testStartDateTime");

      if (!startTime) {
        const now = new Date().getTime();
        localStorage.setItem("testStartTime", now.toString());
      }

      if (!startDateTime) {
        localStorage.setItem(
          "testStartDateTime",
          testStartDateTime.toISOString()
        );
      }

      updateTimer();
      interval = setInterval(updateTimer, 1000);
    }

    return () => clearInterval(interval);
  }, [testData, testStartTime]);

  if (!testData) {
    return <div>No test data available</div>;
  }

  const onFileChange = (info) => {
    setFile(info.file);
  };

  const onFinish = async (values) => {
    const spentTime = CountSpentTime();
    console.log("Spent time", spentTime);
    console.log("Received values of variant: ", values);
    localStorage.removeItem("testStartTime");
    navigate("/home");

    const now = new Date();

    const formData = {
      info: {
        students_name: localStorage.getItem("name"),
        students_surname: localStorage.getItem("surname"),
        start_datetime: localStorage.getItem("testStartDateTime"),
        end_datetime: now.toISOString(),
        variant_id: testData.id,
      },
      answers: Object.entries(values)
        .filter(([key]) => !isNaN(parseInt(key))) // Фильтруем только числовые ключи
        .map(([key, value]) => ({
          variants_task_id: parseInt(key),
          answer: { int: value },
        })),
    };
    console.log("On finish", file);
    if (file) {
      let file_data = new FormData();
      file_data.append("file", file);
      try {
        const result = await sendFileToServer({
          data: file_data,
          variant_id: testData.id,
        });
        console.log("Ответ сервера", result);
      } catch (error) {
        console.error("Не удалось отправить данные на сервер", error);
      }
    }
    console.log(formData);
    localStorage.removeItem("testStartDateTime");
    localStorage.removeItem("name");
    localStorage.removeItem("surname");
    localStorage.removeItem("variant");

    try {
      const answersResult = await PostVariantResult({ requestBody: formData });
      console.log("Ответ сервера на отправку ответов", answersResult);
    } catch (error) {
      console.error("Не удалось отправить ответы на сервер", error);
    }
  };

  return (
    <BasePage>
      <Space direction="vertical" size="middle">
        <h1>{testData.test_info.name}</h1>
        <h2>Оставшееся время: {remainingTime}</h2>
        <Form
          form={form}
          name="create_task_type"
          onFinish={onFinish}
          layout="vertical"
          style={{ maxWidth: 800 }}
        >
          <Space size="middle" direction="vertical">
            {tasks.map((task, index) => {
              return (
                <Card title={`Задание ${index + 1}`} style={{ minWidth: 800 }}>
                  <Space size="middle" direction="vertical">
                    <div>{task.task.description_data}</div>
                    <div>
                      <RenderForm
                        type={task.task.type.condition_forms[0]}
                        data={task.task.condition_data}
                      />
                    </div>
                    <Item name={`${task.id}`} label="Ответ">
                      <RenderForm
                        type={task.task.type.answer_forms[0]}
                        data={""}
                      />
                    </Item>
                  </Space>
                </Card>
              );
            })}
            {/* <Form.Item label="Загрузить PDF файл"> */}
            <Upload beforeUpload={() => false} onChange={onFileChange}>
              <Button>Выбрать файл</Button>
            </Upload>
            {/* </Form.Item> */}
            <Form.Item>
              <Button type="primary" onClick={showModal}>
                Отправить
              </Button>
            </Form.Item>
          </Space>
        </Form>
      </Space>
      <Modal
        title="Подтверждение"
        open={isModalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        okText="Да, завершить"
        cancelText="Отмена"
      >
        <p>Вы уверены, что хотите завершить тестирование?</p>
      </Modal>
    </BasePage>
  );
};

export default VariantPage;
