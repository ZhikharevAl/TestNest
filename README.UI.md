# [![Actions status](https://github.com/ZhikharevAl/xyz-bank/actions/workflows/ruff_check.yml/badge.svg)](https://github.com/ZhikharevAl/xyz-bank/actions/workflows/ruff_check.yml)

# Проект автоматизированного тестирования XYZ Bank

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

Данный проект представляет собой набор автоматизированных тестов для веб-приложения XYZ Bank. Тесты охватывают основные функции управления клиентами, включая добавление новых клиентов, просмотр списка клиентов и удаление клиентов.

## Структура проекта

```
xyz-bank/
│
├── .github/               # Конфигурации GitHub
├── config
│   ├── __init__.py
│   ├── config.py
├── data/                  # Модули для работы с данными
│   ├── __init__.py
│   ├── customer.py
│   ├── generators.py
│   └── providers.py
├── docs/                  # Документация
│   └── attachment/
│   └── ui/
│       ├── TC_001_add_customer_generated_data.md
│       ├── TC_002_sort_customers.md
│       └── TC_003_delete_customers.md
├── pages/                 # Page Object модели
│   ├── __init__.py
│   ├── add_customer_page.py
│   ├── base_page.py
│   └── customer_list_page.py
├── tests/                 # Тестовые модули
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── test_add_customer.py
│   │   ├── test_customer_list.py
│   │   └── test_delete_customer.py
│   └── __init__.py
├── .gitignore
├── conftest.py            # Конфигурация PyTest
├── pyproject.toml         # Конфигурация Ruff
├── pytest.ini             # Конфигурация PyTest
├── README.md
├── requirements.txt       # Зависимости проекта
├── utils.py
```

## Основные функции

- Добавление нового клиента с валидными данными
- Сортировка списка клиентов по имени (по возрастанию и убыванию)
- Удаление клиента со средней длиной имени

## Технологии и инструменты

- Python
- Pytest
- Allure для создания отчетов
- Selenium WebDriver (для взаимодействия с браузером)
- Page Object Pattern для структурирования тестов

## Настройка окружения

1. Убедитесь, что у вас установлен Python 3.10+
2. Склонируйте репозиторий:
   ```
   git clone https://github.com/ZhikharevAl/xyz-bank-customers.git
   cd xyz-bank
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

Для запуска всех тестов используйте команду(параллельный запуск, настройки в [pytest.ini](pytest.ini)):

```
pytest
```

Для запуска конкретного теста:

```
pytest tests/ui/test_add_customer.py
```

Для генерации Allure-отчета:

```
pytest --alluredir=./allure-results
allure serve ./allure-results
```

![Screenshot 2024-09-23 add](docs/attachment/Screenshot%202024-09-23%20005803.png)
![Screenshot 2024-09-23 sort](docs/attachment/Screenshot%202024-09-23%20005857.png)
![Screenshot 2024-09-23 delete](docs/attachment/Screenshot%202024-09-23%20005932.png)
![Screenshot 2024-09-23 history](docs/attachment/Screenshot%202024-09-history.png)
## Структура отчетов

Тесты используют фреймворк Allure для создания подробных отчетов. Каждый тест содержит:

- Описание теста в формате HTML
- Шаги выполнения теста
- Скриншот при падении теста
- Уровень важности теста

## Особенности проекта

- Использование генераторов данных для создания тестовых данных клиентов
- Параметризация тестов для проверки различных сценариев
- Параллельный запуск тестов
- Проверка корректности сортировки путем сравнения программно отсортированного списка с отсортированным через UI
- Документирование тест-кейсов в директории `docs/ui/`