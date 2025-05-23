# 💱 MVP Сервиса P2P-обмена валют

![Docker Required](https://img.shields.io/badge/Docker-обязателен-blue?logo=docker) 
![Status](https://img.shields.io/badge/Статус-в%20разработке-yellow)
![GitHub](https://img.shields.io/badge/Репозиторий-GitHub-black?logo=github)

## 📌 О проекте
Платформа для прямого обмена валют между пользователями (Peer-to-Peer) с интеграцией Telegram-бота и Centrifugo для реального времени.

## 🚀 Быстрый старт

### ⚙️ Требования
- Docker 20.10+
- GNU Make (опционально)

```bash
# 1. Клонировать репозиторий
git clone git@github.com:poolDyy/CashChange.git
cd CashChange

# 2. Настроить окружение (заполните значения в файлах)
cp cicd/centrifugo/.env-example cicd/centrifugo/.env
cp telegram/.env-example telegram/.env
cp backend/.env-example backend/.env

# 3. Запустить сервисы
docker compose up -d --build

# 4. Запустить тесты
docker exec -it backend pytest .
```
## 🛠 Makefile команды

| Команда          | Описание                                  | Полный аналог Docker-команды                          |
|------------------|-------------------------------------------|-------------------------------------------------------|
| `make lint`      | Проверка кода бэкенда через ruff          | `docker exec backend ruff check .`                    |
| `make test`      | Запуск pytest-тестов                      | `docker exec -it backend pytest .`                    |
| `make b-logs`    | Логи бэкенда в реальном времени           | `docker logs -f backend`                              |
| `make t-logs`    | Логи Telegram-бота                        | `docker logs -f telegram`                             |
| `make Start`     | Запуск всех сервисов                      | `docker compose up -d`                                |
| `make Stop`      | Остановка всех сервисов                   | `docker compose stop`                                 |
| `make rmi-backend` | Полная пересборка бэкенда               | `docker stop backend && docker rm backend && docker rmi cashchange-backend` |
| `make rmi-telegram` | Полная пересборка Telegram-бота       | `docker stop telegram && docker rm telegram && docker rmi cashchange-telegram` |

# Ключевые возможности

### Система аутентификации
- **Авторизация по JWT-токенам**
- **Верификация через Telegram**

### Обмен валют
- **Создание и поиск предложений**

### Чат для сделок
- **Встроенная система сообщений**
