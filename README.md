# Как запустить??
1. Скачать [Docker Desktop](https://www.docker.com/products/docker-desktop/)
2. Скачать проект
3. Перейти в папку проекта и в консоли написать команду `make dev`

   (если у вас Windows и возникает ошибка `bash: make: command not found`, то введите команду `docker compose up`)
4. Ждем, пока контейнеры соберутся

   (в логах должно появиться `web-1  | INFO:     Application startup complete.`)
6. Переходим на http://localhost:8000/docs (там лежит документация API)
