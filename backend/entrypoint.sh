#!/bin/sh

# Прерывать выполнение при ошибке
set -e

echo "--- Ожидание готовности базы данных ---"
# Если в docker-compose настроен healthcheck, 
# скрипт просто дождется его завершения.

echo "--- Применение миграций Alembic ---"
alembic upgrade head

echo "--- Запуск сервера Uvicorn ---"
exec uvicorn src.main:app --host 0.0.0.0 --port 8000