# ArticleHub

Полноценное Django-веб-приложение для публикации и управления статьями с комментариями, рейтингом, избранным, ролями пользователей, административной панелью и системой статистики.

## Возможности

- регистрация, вход, выход, смена и восстановление пароля;
- роли `user`, `author`, `admin` с проверками и в интерфейсе, и на сервере;
- CRUD для статей и комментариев;
- модерация комментариев и управление пользователями через Django Admin и dashboard;
- поиск, фильтрация и сортировка статей;
- лайки, дизлайки, избранное и счетчик просмотров;
- загрузка аватара пользователя и обложки статьи;
- агрегированная статистика по статьям, категориям, тегам и авторам;
- экспорт списка статей в CSV;
- Docker + Docker Compose для быстрого запуска.

## Стек

- Python 3.12+
- Django
- PostgreSQL
- Bootstrap 5
- Django Templates
- Docker / Docker Compose

## Структура проекта

```text
articles/
├── apps/
│   ├── articles/
│   ├── comments/
│   ├── core/
│   ├── dashboard/
│   └── users/
├── config/
├── media/
├── static/
├── templates/
├── .env.example
├── docker-compose.yml
├── Dockerfile
├── entrypoint.sh
├── manage.py
├── README.md
└── requirements.txt
```

## Сущности

- `User` - кастомная модель пользователя на основе `AbstractUser`
- `Category` - категории статей
- `Tag` - теги
- `Article` - статьи
- `Comment` - комментарии
- `Vote` - лайки и дизлайки
- `Favorite` - избранные статьи

## Запуск через Docker

1. Скопируйте настройки окружения:

```bash
cp .env.example .env
```

2. Запустите контейнеры:

```bash
docker compose up --build
```

3. Откройте приложение:

```text
http://localhost:8000
```

## Что делает контейнер при старте

- ожидает доступность PostgreSQL;
- выполняет миграции;
- собирает статику;
- по переменной `LOAD_DEMO_DATA=True` загружает демонстрационные данные;
- запускает Gunicorn.

## Демо-учетные записи

После запуска с `LOAD_DEMO_DATA=True` доступны:

- администратор: `admin / admin12345`
- авторы: `author1 / author12345`, `author2 / author12345`, `author3 / author12345`
- пользователи: `user1 / user12345`, `user2 / user12345`, `user3 / user12345`

## Основные маршруты

- `/` - главная страница
- `/articles/` - список статей
- `/articles/create/` - создание статьи
- `/articles/mine/` - мои статьи
- `/articles/favorites/` - избранное
- `/users/register/` - регистрация
- `/users/login/` - вход
- `/users/profile/` - профиль
- `/dashboard/` - dashboard администратора
- `/admin/` - стандартная административная панель Django

## Тестовые данные

Для ручной загрузки демо-данных:

```bash
python manage.py seed_demo_data
```

## Экспорт данных

- CSV-экспорт списка статей: `/articles/export/csv/`
- подготовлен каркас сервиса `apps/articles/pdf_export.py` для дальнейшего PDF-экспорта одной статьи

## Замечания по ролям

- гость может только просматривать и искать статьи;
- пользователь может комментировать, голосовать и добавлять статьи в избранное;
- автор может создавать, редактировать и удалять только свои статьи;
- администратор имеет полный доступ к dashboard, экспорту и модерации.

## Полезные команды без Docker

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```
