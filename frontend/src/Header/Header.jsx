import React from 'react';
import './Header.css'; // Убедитесь, что у вас есть этот CSS файл

export default function Header() {
  const handleLoginClick = () => {
    // Обработка нажатия на кнопку Log In
    console.log('Log In button clicked');
  };

  return (
    <header className="header">
      <nav className="navbar">
        {/* Здесь может быть логотип или другие элементы навигации */}
        <div className="login-button-container">
          <button onClick={handleLoginClick} className="login-button">Log In</button>
        </div>
      </nav>
    </header>
  );
};
