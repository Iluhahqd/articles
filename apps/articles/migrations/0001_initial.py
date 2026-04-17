import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="Название")),
                ("slug", models.SlugField(blank=True, max_length=140, unique=True, verbose_name="Slug")),
                ("description", models.TextField(blank=True, verbose_name="Описание")),
            ],
            options={
                "verbose_name": "Категория",
                "verbose_name_plural": "Категории",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True, verbose_name="Название")),
                ("slug", models.SlugField(blank=True, max_length=100, unique=True, verbose_name="Slug")),
            ],
            options={
                "verbose_name": "Тег",
                "verbose_name_plural": "Теги",
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255, verbose_name="Заголовок")),
                ("slug", models.SlugField(blank=True, max_length=280, unique=True, verbose_name="Slug")),
                ("short_description", models.CharField(max_length=300, verbose_name="Краткое описание")),
                ("content", models.TextField(verbose_name="Содержание")),
                ("cover_image", models.ImageField(blank=True, null=True, upload_to="covers/", verbose_name="Обложка")),
                ("status", models.CharField(choices=[("draft", "Черновик"), ("published", "Опубликовано")], default="draft", max_length=20, verbose_name="Статус")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("updated_at", models.DateTimeField(auto_now=True, verbose_name="Обновлено")),
                ("published_at", models.DateTimeField(blank=True, null=True, verbose_name="Опубликовано")),
                ("views_count", models.PositiveIntegerField(default=0, verbose_name="Просмотры")),
                ("author", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="articles", to=settings.AUTH_USER_MODEL, verbose_name="Автор")),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="articles", to="articles.category", verbose_name="Категория")),
                ("tags", models.ManyToManyField(blank=True, related_name="articles", to="articles.tag", verbose_name="Теги")),
            ],
            options={
                "verbose_name": "Статья",
                "verbose_name_plural": "Статьи",
                "ordering": ("-published_at", "-created_at"),
            },
        ),
        migrations.CreateModel(
            name="Vote",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("value", models.SmallIntegerField(choices=[(1, "Лайк"), (-1, "Дизлайк")], verbose_name="Значение")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("article", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="votes", to="articles.article", verbose_name="Статья")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="votes", to=settings.AUTH_USER_MODEL, verbose_name="Пользователь")),
            ],
            options={
                "verbose_name": "Голос",
                "verbose_name_plural": "Голоса",
            },
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Создано")),
                ("article", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorited_by", to="articles.article", verbose_name="Статья")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="favorite_articles", to=settings.AUTH_USER_MODEL, verbose_name="Пользователь")),
            ],
            options={
                "verbose_name": "Избранное",
                "verbose_name_plural": "Избранное",
            },
        ),
        migrations.AddConstraint(
            model_name="vote",
            constraint=models.UniqueConstraint(fields=("article", "user"), name="unique_article_vote"),
        ),
        migrations.AddConstraint(
            model_name="favorite",
            constraint=models.UniqueConstraint(fields=("user", "article"), name="unique_favorite_article"),
        ),
    ]
