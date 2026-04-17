from django.contrib import admin

from apps.comments.models import Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("article", "author", "created_at", "is_approved")
    list_filter = ("is_approved", "created_at")
    search_fields = ("text", "article__title", "author__username")
    autocomplete_fields = ("article", "author")
