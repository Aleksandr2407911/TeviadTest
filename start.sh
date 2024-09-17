#!/bin/bash
set -e  # Завершить выполнение при ошибке

# Ждем, пока база данных будет доступна
while !</dev/tcp/db/5432; do
    sleep 1;
done;

# Выполняем миграции
poetry run alembic upgrade head

# Запускаем Uvicorn с вашим приложением FastAPI через Poetry
exec poetry run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload