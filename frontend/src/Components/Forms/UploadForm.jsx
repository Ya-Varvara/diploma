import React from 'react';
import { useState } from 'react';
import { Upload, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';

const PdfUpload = () => {
    const [selectedFile, setSelectedFile] = useState(); // Состояние для хранения файла
  
    const checkFileType = (file) => {
      const isPdf = file.type === 'application/pdf';
      if (!isPdf) {
        message.error('Вы можете загрузить только PDF файлы!');
      }
      return isPdf || Upload.LIST_IGNORE; // Прекратить загрузку, если файл не PDF
    };
  
    const handleFileChange = (info) => {
      if (info.file.status === 'done') {
        message.success(`${info.file.name} файл успешно загружен.`);
        setSelectedFile(info.file.originFileObj); // Сохраняем оригинальный объект файла
      } else if (info.file.status === 'error') {
        message.error(`${info.file.name} ошибка загрузки файла.`);
      }
    };
  
    const sendFileAsBinary = () => {
      if (selectedFile) {
        const reader = new FileReader();
        reader.onload = function(e) {
          console.log(e.target.result); // Выводим бинарные данные в консоль
        };
        reader.readAsArrayBuffer(selectedFile); // Читаем файл как бинарные данные
      }
    };
  
    return (
      <>
        <Upload
          beforeUpload={checkFileType}
          onChange={handleFileChange}
          showUploadList={false}
        >
          <Button icon={<UploadOutlined />}>Выбрать PDF</Button>
        </Upload>
        <Button
          type="primary"
          onClick={sendFileAsBinary}
          disabled={!selectedFile}
          style={{ marginTop: '16px' }}
        >
          Отправить данные в консоль
        </Button>
      </>
    );
  };
export default PdfUpload;