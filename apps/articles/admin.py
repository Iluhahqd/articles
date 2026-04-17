from django.contrib import admin

from apps.articles.models import Article, Category, Favorite, Tag, Vote


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "status", "published_at", "views_count")
    list_filter = ("status", "category", "tags")
    search_fields = ("title", "short_description", "content")
    prepopulated_fields = {"slug": ("title",)}
    autocomplete_fields = ("author", "category", "tags")
    date_hierarchy = "published_at"


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "value", "created_at")
    list_filter = ("value",)
    autocomplete_fields = ("article", "user")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("article", "user", "created_at")
    autocomplete_fields = ("article", "user")
