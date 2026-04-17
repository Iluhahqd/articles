from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = "user", "Пользователь"
        AUTHOR = "author", "Автор"
        ADMIN = "admin", "Администратор"

    email = models.EmailField("Email", unique=True)
    avatar = models.ImageField("Аватар", upload_to="avatars/", blank=True, null=True)
    role = models.CharField("Роль", max_length=20, choices=Roles.choices, default=Roles.USER)
    bio = models.TextField("О себе", blank=True)

    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
        ordering = ("username",)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if self.role == self.Roles.ADMIN:
            self.is_staff = True
        return super().save(*args, **kwargs)

    @property
    def is_author(self):
        return self.role in {self.Roles.AUTHOR, self.Roles.ADMIN} or self.is_staff or self.is_superuser

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN or self.is_staff or self.is_superuser
