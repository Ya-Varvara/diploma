import React, { useEffect, useState } from "react";
import { Spin, message } from "antd";
import { baseURL } from "../Handlers/API";

const FileViewer = ({ fileId }) => {
  const [fileUrl, setFileUrl] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchFile = async () => {
      setLoading(true);
      try {
        const response = await fetch(`${baseURL}/upload/${fileId}/`);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const blob = await response.blob();
        const fileUrl = URL.createObjectURL(blob);
        setFileUrl(fileUrl);
      } catch (error) {
        message.error("Ошибка при загрузке файла: " + error.message);
      } finally {
        setLoading(false);
      }
    };

    if (fileId) {
      fetchFile();
    }
    return () => {
      URL.revokeObjectURL(fileUrl);
    };
  }, [fileId]);

  if (loading) {
    return <Spin size="large" />;
  }

  return <iframe src={fileUrl} style={{ width: "100%", height: "90vh" }} />;
};

export default FileViewer;
