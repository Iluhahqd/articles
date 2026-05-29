# Deployment

Инструкция рассчитана на VPS/сервер с Docker и Docker Compose.

## 1. Подготовить сервер

```bash
sudo apt update
sudo apt install -y docker.io docker-compose-plugin git
sudo systemctl enable --now docker
```

## 2. Загрузить проект

Вариант через Git:

```bash
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ> articles
cd articles
```

Или загрузите папку проекта на сервер через панель хостинга/SFTP.

## 3. Создать `.env`

```bash
cp .env.production.example .env
nano .env
```

Для production обязательно поменяйте:

```env
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=replace-with-long-random-secret
DJANGO_ALLOWED_HOSTS=example.com,www.example.com,server-ip
DJANGO_CSRF_TRUSTED_ORIGINS=https://example.com,https://www.example.com,http://server-ip
POSTGRES_DB=articles_db
POSTGRES_USER=articles_user
POSTGRES_PASSWORD=replace-with-strong-password
POSTGRES_HOST=db
POSTGRES_PORT=5432
LOAD_INITIAL_DATA=False
```

## 4. Запустить

```bash
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

Проверить контейнеры:

```bash
docker compose -f docker-compose.prod.yml ps
```

Посмотреть логи:

```bash
docker compose -f docker-compose.prod.yml logs -f web
```

## 5. Обновление после изменений

```bash
git pull
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d
```

## HTTPS

Этот compose открывает сайт на HTTP, порт `80`. Для HTTPS проще всего подключить домен к серверу и поставить внешний reverse proxy с Let's Encrypt, например Caddy, Traefik или nginx-proxy/acme-companion.
