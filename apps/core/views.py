from django.db.models import Count
from django.views.generic import TemplateView

from apps.articles.models import Article, Category, Tag


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published = Article.objects.published().with_engagement().select_related("author", "category").prefetch_related("tags")
        context["latest_articles"] = published[:6]
        context["popular_articles"] = published.order_by("-rating", "-views_count")[:5]
        context["discussed_articles"] = published.order_by("-comments_count", "-published_at")[:5]
        context["categories"] = Category.objects.annotate(article_total=Count("articles")).order_by("-article_total", "name")[:8]
        context["tags"] = Tag.objects.annotate(article_total=Count("articles")).order_by("-article_total", "name")[:16]
        return context
