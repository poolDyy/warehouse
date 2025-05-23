# Сервис по контролю объектов на складе

![Docker Required](https://img.shields.io/badge/Docker-обязателен-blue?logo=docker) 
![Status](https://img.shields.io/badge/Статус-в%20разработке-yellow)
![GitHub](https://img.shields.io/badge/Репозиторий-GitHub-black?logo=github)

## 📌 О проекте
Платформа позволяющая осуществлять контроль и учет объектов хранящихся на складе.  
URL документации: /api/docs/  
Основные функции:
 - CRUD Пользователя 
 - CRUD Склада
 - CRUD Материалов 
 - CRUD Продуктов

## 🚀 Быстрый старт

### ⚙️ Требования
- Docker 20.10+
- GNU Make (опционально)

```bash
# 1. Клонировать репозиторий
git clone git@github.com:poolDyy/warehouse.git
cd warehouse

# 2. Настроить окружение (заполните значения в файлах)
cp backend/.env-example backend/.env

# 3. Запустить сервисы
docker compose up -d --build

# 4. Запустить тесты
docker exec -it backend pytest .
```
## 🛠 Makefile команды

| Команда          | Описание                                  | Полный аналог Docker-команды                                                  |
|------------------|-------------------------------------------|-------------------------------------------------------------------------------|
| `make lint`      | Проверка кода бэкенда через ruff          | `docker exec wh-backend ruff check .`                                         |
| `make test`      | Запуск pytest-тестов                      | `docker exec -it wh-backend pytest .`                                         |
| `make b-logs`    | Логи бэкенда в реальном времени           | `docker logs -f wh-backend`                                                   |
| `make Start`     | Запуск всех сервисов                      | `docker compose up -d`                                                        |
| `make Stop`      | Остановка всех сервисов                   | `docker compose stop`                                                         |
| `make rmi-backend` | Полная пересборка бэкенда               | `docker stop wh-backend && docker rm wh-backend && docker rmi wh-wh-backend ` |

