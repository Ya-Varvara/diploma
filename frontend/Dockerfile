# Устанавливаем официальный образ Node.js в качестве базового
FROM node:alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY package*.json ./
COPY vite.config.js ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код фронтенда в контейнер
COPY . .

# Строим приложение для продакшена
# RUN npm run build

# Запускаем сервер разработки
CMD ["npm", "run", "dev"]

# Открываем порт 5173
EXPOSE 3000
