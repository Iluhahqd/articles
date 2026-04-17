from django.conf import settings
from django.db import models
from django.db.models import Count, Q, Sum
from django.urls import reverse
from django.utils import timezone

from apps.core.utils import unique_slugify


class Category(models.Model):
    name = models.CharField("Название", max_length=120, unique=True)
    slug = models.SlugField("Slug", max_length=140, unique=True, blank=True)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("articles:category_detail", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField("Название", max_length=80, unique=True)
    slug = models.SlugField("Slug", max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
        ordering = ("name",)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.name)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("articles:tag_detail", kwargs={"slug": self.slug})


class ArticleQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Article.Status.PUBLISHED, published_at__isnull=False)

    def with_engagement(self):
        return self.annotate(
            rating=Sum("votes__value", default=0),
            comments_count=Count("comments", filter=Q(comments__is_approved=True), distinct=True),
            favorites_count=Count("favorited_by", distinct=True),
        )

    def searchable(self, query):
        if not query:
            return self
        return self.filter(Q(title__icontains=query) | Q(short_description__icontains=query) | Q(content__icontains=query))


class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Черновик"
        PUBLISHED = "published", "Опубликовано"

    title = models.CharField("Заголовок", max_length=255)
    slug = models.SlugField("Slug", max_length=280, unique=True, blank=True)
    short_description = models.CharField("Краткое описание", max_length=300)
    content = models.TextField("Содержание")
    cover_image = models.ImageField("Обложка", upload_to="covers/", blank=True, null=True)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.DRAFT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="articles", verbose_name="Автор")
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, blank=True, null=True, related_name="articles", verbose_name="Категория")
    tags = models.ManyToManyField("Tag", blank=True, related_name="articles", verbose_name="Теги")
    created_at = models.DateTimeField("Создано", auto_now_add=True)
    updated_at = models.DateTimeField("Обновлено", auto_now=True)
    published_at = models.DateTimeField("Опубликовано", blank=True, null=True)
    views_count = models.PositiveIntegerField("Просмотры", default=0)

    objects = ArticleQuerySet.as_manager()

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        ordering = ("-published_at", "-created_at")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            unique_slugify(self, self.title)
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        if self.status == self.Status.DRAFT:
            self.published_at = None
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("articles:detail", kwargs={"slug": self.slug})


class Vote(models.Model):
    VALUE_CHOICES = ((1, "Лайк"), (-1, "Дизлайк"))

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="votes", verbose_name="Статья")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes", verbose_name="Пользователь")
    value = models.SmallIntegerField("Значение", choices=VALUE_CHOICES)
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Голос"
        verbose_name_plural = "Голоса"
        constraints = [
            models.UniqueConstraint(fields=("article", "user"), name="unique_article_vote"),
        ]

    def __str__(self):
        return f"{self.user} -> {self.article} ({self.value})"


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorite_articles",
        verbose_name="Пользователь",
    )
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="favorited_by", verbose_name="Статья")
    created_at = models.DateTimeField("Создано", auto_now_add=True)

    class Meta:
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(fields=("user", "article"), name="unique_favorite_article"),
        ]

    def __str__(self):
        return f"{self.user} -> {self.article}"
