# Устанавливаем официальный образ Node.js в качестве базового
FROM node:18-alpine

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файлы package.json
COPY package.json ./
# Устанавливаем зависимости
RUN npm install
RUN npm install js-cookie
# Копируем исходный код фронтенда в контейнер
COPY . .

# Строим приложение для продакшена
# RUN npm run build

# Открываем порт 3000
EXPOSE 3000

# Запускаем сервер разработки
CMD ["npm", "run", "dev"]
