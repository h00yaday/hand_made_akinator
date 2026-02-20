#!/bin/sh

# Прерываем выполнение скрипта, если какая-то команда упала с ошибкой
set -e

# Здесь в будущем будет команда миграций:
# echo "Running migrations..."
# alembic upgrade head

# Запускаем сам сервер (exec подменяет процесс скрипта на процесс uvicorn)
echo "Starting backend server..."
exec uvicorn src.main:app --host 0.0.0.0 --port 8000