# Как запустить??
1. Скачать [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Скачать или клонировать проект
3. Перейти в папку проекта и в консоли написать команду `make dev`

   (если у вас Windows и возникает ошибка `bash: make: command not found`, то введите команду `docker compose up --build`)
4. Ждем, пока контейнеры соберутся

   В логах должно появиться
   ```
   frontend-1  | > frontend@0.0.0 dev
   frontend-1  | > vite
   frontend-1  | 
   frontend-1  | Re-optimizing dependencies because vite config has changed
   frontend-1  | 
   frontend-1  |   VITE v5.1.4  ready in 770 ms
   frontend-1  | 
   frontend-1  |   ➜  Local:   http://localhost:3000/
   frontend-1  |   ➜  Network: http://172.19.0.3:3000/
   api-1       | INFO:     Started server process [9]
   api-1       | INFO:     Waiting for application startup.
   api-1       | INFO:     Application startup complete.
   ```

## Сейчас доступно:
### API 
Адрес http://localhost:8000/docs
### Bеб-приложение 
Адрес http://localhost:3000 
Веб-приложение не имеет связи с сервером, поэтому пока нет логики работы
Доступны следующие страницы:
1. Домашняя страница http://localhost:3000/
2. Страница регистрации http://localhost:3000/register
3. Страница авторизации http://localhost:3000/login
