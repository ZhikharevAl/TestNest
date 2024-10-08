# [![Ruff Linter](https://github.com/ZhikharevAl/TestNest/actions/workflows/ruff_check.yml/badge.svg)](https://github.com/ZhikharevAl/TestNest/actions/workflows/ruff_check.yml)
# Проект автоматизированного тестирования API

## Оглавление
- [Описание проекта](#описание-проекта)
- [Структура проекта](#структура-проекта)
- [Основные функции](#основные-функции)
- [Технологии и инструменты](#технологии-и-инструменты)
- [Настройка окружения](#настройка-окружения)
- [Запуск тестов](#запуск-тестов)
- [Структура отчетов](#структура-отчетов)
- [Особенности проекта](#особенности-проекта)

## Описание проекта

Данный проект представляет собой набор автоматизированных тестов для API управления сущностями. Тесты охватывают основные CRUD операции, включая создание, чтение, обновление и удаление сущностей.

## Структура проекта

```
project_root/
│
├── services/
│   └── entity/
│       ├── api_client.py
│       ├── http_client.py
│       ├── models/
│       │   └── entity_model.py
│       └── payloads.py
│
├── tests/
│   └── api/
│      └── test_api.py
│
├── utils/
│   └── allure_utils.py
│
│
├── .gitignore
├── conftest.py
├── pytest.ini
├── README.md
└── requirements.txt
```

## Основные функции

- Создание новой сущности с валидными данными
- Получение информации о существующей сущности
- Обновление данных сущности
- Удаление сущности
- Получение списка всех сущностей

## Технологии и инструменты

- Python 3.10+
- Pytest
- Requests
- Allure для создания отчетов
- Faker для генерации тестовых данных
- GitHub Actions для непрерывной интеграции

## Настройка окружения

1. Убедитесь, что у вас установлен Python 3.10+
2. Склонируйте репозиторий:
   ```
   git clone https://github.com/ZhikharevAl/TestNest.git
   ```
3. Создайте виртуальное окружение и активируйте его:
   ```
   python -m venv venv
   source venv/bin/activate  # Для Linux/Mac
   venv\Scripts\activate     # Для Windows
   ```
4. Установите зависимости:
   ```
   pip install -r requirements.txt
   ```

## Запуск тестов

Для запуска всех тестов используйте команду:

```
pytest
```

Для запуска конкретного теста:

```
pytest tests/test_api.py::TestEntityAPI::test_create_entity
```

Для генерации Allure-отчета:

```
pytest --alluredir=./allure-results
allure serve ./allure-results
```
Запуск в github actions через [ngrok](https://ngrok.com/)
![Screenshot 2024-09-23 add](docs/attachment/Screenshot%202024-09-25%20062219.png)
![Screenshot 2024-09-23 add](docs/attachment/Screenshot%202024-09-28%20055121.png)

## Структура отчетов

Тесты используют фреймворк Allure для создания подробных отчетов. Каждый тест содержит:

- Описание теста
- Шаги выполнения теста
- Запросы и ответы API
- Уровень важности теста

## Особенности проекта

- Использование Faker для генерации тестовых данных
- Автоматическое логирование запросов и ответов API
- Проверка корректности данных в ответах API
- Использование GitHub Actions для автоматического запуска тестов при push и pull request