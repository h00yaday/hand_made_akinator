# Шпаргалка разработчика (Cheatsheet)

## 🐳 Docker (Основа)

**Запустить проект (с пересборкой):**
Самая частая команда. Делайте это, если pull-нули обновления или добавили библиотеку.

```bash
docker-compose up --build
```


**Просто запустить (быстро):**

**Bash**

```
docker-compose up
```

**Остановить всё:**

**Bash**

```
docker-compose down
```

**Посмотреть логи (если что-то упало):**

**Bash**

```
docker-compose logs -f
# Или конкретного сервиса:
docker-compose logs -f backend
```


**Зайти внутрь контейнера (как SSH):** Если нужно запустить скрипт руками или проверить файлы внутри.

**Bash**

```
# Для бэкенда
docker exec -it akinator_backend bash

# Для базы данных
docker exec -it akinator_db bash
```


## 🐍 Python & Backend

**Я добавил новую библиотеку (`pip install X`). Что делать?**

1. Добавь её название в `backend/requirements.txt`.
2. Пересобери контейнер: `docker-compose up --build`.

**Как подключиться к БД из кода?** Используй переменные окружения (они уже прокинуты в Docker):

* `DB_HOST`: db
* `DB_USER`: user
* `DB_PASS`: password
* `DB_NAME`: akinator\_db

---

## 🐘 База Данных

**Как подключиться через DBeaver / pgAdmin?**

* **Host:** localhost
* **Port:** 5432 (или тот, что в docker-compose, если меняли)
* **User:** user
* **Password:** password
* **Database:** akinator\_db

**Как сбросить базу данных (удалить все данные)?** Осторожно! Удаляет всё!

**Bash**

```
docker-compose down -v
docker-compose up --build
```

---

## 🐙 Git (Ситуации)

**Хочу начать новую задачу:**

**Bash**

```
git checkout main
git pull origin main
git checkout -b feat/my-new-task
```

**Я работаю, а в `main` вышли обновления. Хочу их себе:**

**Bash**

```
# Находясь в своей ветке
git fetch origin
git rebase origin/main
# Если есть конфликты — решаем их, затем:
# git add .
# git rebase --continue
```
