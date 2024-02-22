# Устанавливаем официальный образ Node.js в качестве базового
FROM node:16-alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы package.json и package-lock.json
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем исходный код фронтенда в контейнер
COPY . .

# Строим приложение для продакшена
RUN npm run build

# Запускаем сервер разработки
CMD ["npm", "start"]

# Открываем порт 3000
EXPOSE 3000
