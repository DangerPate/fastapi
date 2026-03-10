# 📜 Реестр лицензий и сертификатов

<div align="center">

Веб-приложение для учёта лицензий, сертификатов и разрешительных документов

[![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Vue](https://img.shields.io/badge/Vue-3.5.29-green?logo=vue.js)](https://vuejs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-blue?logo=typescript)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue?logo=postgresql)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

</div>

---

## 📖 О проекте

**Реестр лицензий и сертификатов** — это полнофункциональное веб-приложение для централизованного учёта и мониторинга лицензий, сертификатов и иных разрешительных документов.

### ✨ Особенности

- 🎨 **Современный тёмный интерфейс** для комфортной работы
- 🔄 **Автоматическое обновление статусов** документов (активен / скоро истекает / истёк)
- 📊 **Наглядная визуализация** сроков действия
- 🔔 **Уведомления** о критических изменениях
- 🚀 **SPA-архитектура** с быстрым откликом интерфейса

---

## 🛠 Технологический стек

| Бэкенд | Фронтенд |
|--------|----------|
| ![Python](https://img.shields.io/badge/Python-3.14-blue?logo=python) FastAPI | ![Vue](https://img.shields.io/badge/Vue-3.5.29-green?logo=vue.js) Vue 3 (Composition API) |
| ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-green) SQLAlchemy | ![TypeScript](https://img.shields.io/badge/TypeScript-5.9.3-blue?logo=typescript) TypeScript |
| ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-blue?logo=postgresql) PostgreSQL | ![Vite](https://img.shields.io/badge/Vite-Bundler-purple?logo=vite) Vite |
| ![APScheduler](https://img.shields.io/badge/APScheduler-Tasks-orange) APScheduler | ![Axios](https://img.shields.io/badge/Axios-HTTP-blue?logo=axios) Axios |
| ![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-yellow) Uvicorn | ![Vue Router](https://img.shields.io/badge/Vue_Router-4-green) Vue Router |

---

## 📋 Требования

| Компонент | Версия |
|-----------|--------|
| Python | 3.14 |
| Node.js | 24 |
| PostgreSQL | 18 |
| npm | 11 |

---

## 🚀 Установка и запуск

### 1️⃣ Клонирование репозитория

```bash
git clone https://github.com/DangerPate/fastapi.git
cd project
```

### 2️⃣ Настройка базы данных

```sql
CREATE DATABASE db;
```

> ⚠️ **Важно:** Измените параметры подключения в `backend/database.py` при необходимости.  
> **По умолчанию:** `postgresql://postgres:postgres@localhost:5432/db`

---

### 3️⃣ Бэкенд

```bash
cd backend

# Создание виртуального окружения (рекомендуется)
python -m venv venv

# Активация
source venv/bin/activate           # Linux/Mac
# или
venv\Scripts\activate              # Windows

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера разработки
uvicorn main:app --reload --port 8000
```

| Описание | URL |
|----------|-----|
| API | http://localhost:8000 |
| Swagger Docs | http://localhost:8000/docs |

---

### 4️⃣ Фронтенд

> ⚡ Запускается в **отдельном терминале**

```bash
cd frontend
npm install
npm run dev
```

| Описание | URL |
|----------|-----|
| Frontend | http://localhost:5173 |

> 💡 В режиме разработки запросы к API проксируются на бэкенд (настроено в `vite.config.ts`)

---

## 📦 Сборка для продакшена (монолит)

Приложение может работать как единое целое: бэкенд раздаёт статические файлы фронтенда.

### Шаг 1: Сборка фронтенда

```bash
cd frontend
npm run build
```

> 📁 Собранные файлы появятся в папке `frontend/dist`

### Шаг 2: Запуск бэкенда со статикой

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

| Описание | URL |
|----------|-----|
| Приложение | http://localhost:8000 |

> 🔍 Все маршруты, кроме начинающихся с `/api`, будут обслуживаться фронтендом.  
> ✅ Убедитесь, что путь к папке `dist` в `backend/main.py` корректен (по умолчанию: `../frontend/dist`)

---

## 🔐 Переменные окружения

Для продакшена рекомендуется использовать переменные окружения:

```python
# backend/database.py
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/db")
```

```bash
# Запуск с переменной окружения
DATABASE_URL="postgresql://user:password@host:port/dbname" uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## ⏰ Планировщик задач

В бэкенде реализован **автоматический пересчёт статусов** документов:

| Статус | Описание |
|--------|----------|
| 🟢 Активный | Документ действителен |
| 🟡 Скоро истекает | Осталось **менее 7 дней** |
| 🔴 Истёк | Срок действия истёк |

- 🔄 Задача запускается **каждые 24 часа** автоматически
- 🖐️ Доступен **ручной запуск** через API:

```http
POST /admin/run-status-update
```

---

## 📁 Структура проекта

```
project/
├── backend/                    # Бэкенд FastAPI
│   ├── main.py                 # Точка входа, роуты
│   ├── database.py             # Подключение к БД, сессии
│   ├── models.py               # Модели SQLAlchemy
│   ├── schemas.py              # Pydantic-схемы
│   ├── crud.py                 # Операции с БД
│   ├── requirements.txt        # Зависимости Python
│   └── ...
│
├── frontend/                   # Фронтенд Vue
│   ├── public/                 # Статика
│   ├── src/
│   │   ├── views/              # Страницы
│   │   ├── components/         # Компоненты
│   │   ├── services/           # API-клиент
│   │   ├── types/              # Интерфейсы TypeScript
│   │   ├── constants/          # Константы
│   │   ├── router/             # Маршрутизация
│   │   └── styles/             # Глобальные стили
│   ├── index.html
│   ├── package.json
│   └── ...
│
└── README.md
```



