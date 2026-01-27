# 1. Базовый образ Python (легкий)
FROM python:3.9-slim

# 2. Рабочая папка внутри контейнера
WORKDIR /app

# 3. Копируем файл зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем весь проект
COPY . .

# 5. Сообщаем, что контейнер слушает порт 5000
EXPOSE 5000

# 6. Запускаем через Gunicorn (Продакшн-сервер)
# --bind 0.0.0.0:5000 : слушать все адреса на порту 5000
# run:app : файл run.py, объект app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "run:app"]