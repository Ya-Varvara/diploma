import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Для навигации
import Header from '../Header/Header'; // Импортируем Header
import './HomePage.css'; // Создайте этот CSS файл для стилизации

const HomePage = () => {
  const [uuid, setUuid] = useState('');
  const navigate = useNavigate();

  const handleUuidChange = (event) => {
    setUuid(event.target.value);
  };

  const handleGoButtonClick = () => {
    // Здесь может быть логика проверки UUID
    navigate('/another-page'); // Перенаправляем пользователя
  };

  const handleRegisterClick = () => {
    navigate('/register'); // Перенаправление на страницу регистрации
  };

  return (

    <div className="home-page">
      <Header />
      <div className="main-content">
      <div className="uuid-form-container">
        <input
          type="text"
          value={uuid}
          onChange={handleUuidChange}
          placeholder="Enter UUID"
          className="uuid-input"
        />
        <button onClick={handleGoButtonClick} className="go-button">Go</button>
      </div>
      <button onClick={handleRegisterClick} className="register-button">Register</button>
    </div>
    </div>
  );
};

export default HomePage;
