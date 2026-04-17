import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from apps.articles.models import Article, Category, Favorite, Tag, Vote
from apps.comments.models import Comment


class Command(BaseCommand):
    help = "Заполняет проект демонстрационными данными для курсовой работы."

    def handle(self, *args, **options):
        User = get_user_model()

        admin_user, _ = User.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "role": User.Roles.ADMIN,
                "is_staff": True,
                "is_superuser": True,
                "first_name": "Site",
                "last_name": "Admin",
            },
        )
        admin_user.set_password("admin12345")
        admin_user.save()

        authors = []
        for idx in range(1, 4):
            author, _ = User.objects.get_or_create(
                username=f"author{idx}",
                defaults={
                    "email": f"author{idx}@example.com",
                    "role": User.Roles.AUTHOR,
                    "first_name": f"Автор {idx}",
                    "bio": "Пишет статьи о технологиях, разработке и аналитике.",
                },
            )
            author.set_password("author12345")
            author.save()
            authors.append(author)

        readers = []
        for idx in range(1, 4):
            reader, _ = User.objects.get_or_create(
                username=f"user{idx}",
                defaults={
                    "email": f"user{idx}@example.com",
                    "role": User.Roles.USER,
                    "first_name": f"Пользователь {idx}",
                    "bio": "Читает статьи и участвует в обсуждениях.",
                },
            )
            reader.set_password("user12345")
            reader.save()
            readers.append(reader)

        categories = []
        for name in ["Python", "Django", "DevOps", "Frontend", "Data Science"]:
            category, _ = Category.objects.get_or_create(
                name=name,
                defaults={"description": f"Материалы по теме {name}."},
            )
            categories.append(category)

        tags = []
        for name in ["backend", "postgresql", "docker", "bootstrap", "testing", "api", "deploy"]:
            tag, _ = Tag.objects.get_or_create(name=name)
            tags.append(tag)

        article_payloads = [
            (
                "Архитектура Django-приложения для публикации статей",
                "Как логично разделить проект на приложения, сервисы и шаблоны.",
            ),
            (
                "Как организовать модерацию комментариев",
                "Практический подход к ролям пользователей и контролю доступа.",
            ),
            (
                "Bootstrap 5 для аккуратного интерфейса курсового проекта",
                "Собираем чистый и понятный UI без лишней перегруженности.",
            ),
            (
                "Docker Compose для локального запуска Django и PostgreSQL",
                "Настройка контейнеров, переменных окружения и миграций.",
            ),
            (
                "Как считать рейтинг статьи и вовлеченность аудитории",
                "Используем агрегирующие функции ORM для аналитики контента.",
            ),
            (
                "Поиск и фильтрация материалов в контентной платформе",
                "Делаем удобный каталог статей с сортировками и тегами.",
            ),
        ]

        created_articles = []
        for idx, (title, short_description) in enumerate(article_payloads, start=1):
            author = authors[(idx - 1) % len(authors)]
            category = categories[(idx - 1) % len(categories)]
            article, _ = Article.objects.get_or_create(
                title=title,
                defaults={
                    "short_description": short_description,
                    "content": (
                        f"{title}\n\n"
                        "Этот материал создан как демонстрационная публикация для курсового проекта. "
                        "Он показывает работу статей, комментариев, рейтинга и аналитики в Django-приложении.\n\n"
                        "В статье описаны структура проекта, роли пользователей, поиск, фильтрация, "
                        "модерация контента и экспорт данных."
                    ),
                    "status": Article.Status.PUBLISHED,
                    "author": author,
                    "category": category,
                    "views_count": random.randint(20, 160),
                },
            )
            article.tags.set(random.sample(tags, k=3))
            created_articles.append(article)

        for article in created_articles:
            for reader in readers:
                Vote.objects.update_or_create(
                    article=article,
                    user=reader,
                    defaults={"value": random.choice([1, 1, 1, -1])},
                )
                Favorite.objects.get_or_create(article=article, user=reader)
                Comment.objects.get_or_create(
                    article=article,
                    author=reader,
                    text=f"Интересная статья про {article.category.name.lower()}. Спасибо за материал!",
                    defaults={"is_approved": True},
                )

        self.stdout.write(self.style.SUCCESS("Демо-данные успешно созданы."))
