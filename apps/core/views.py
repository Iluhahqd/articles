from django.db.models import Count, Q, Sum
from django.views.generic import TemplateView

from apps.articles.models import Article, Category, Tag
from apps.comments.models import Comment
from apps.users.models import User


class HomeView(TemplateView):
    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        published = Article.objects.published().with_engagement().select_related("author", "category").prefetch_related("tags")
        hero_article = published.order_by("-views_count", "-rating", "-published_at").first()
        context["latest_articles"] = published[:6]
        context["popular_articles"] = published.order_by("-rating", "-views_count")[:5]
        context["discussed_articles"] = published.order_by("-comments_count", "-published_at")[:5]
        context["hero_article"] = hero_article
        context["featured_articles"] = published.exclude(pk=getattr(hero_article, "pk", None)).order_by("-published_at", "-views_count")[:3]
        context["recent_comments"] = (
            Comment.objects.filter(is_approved=True)
            .select_related("author", "article")
            .order_by("-created_at")[:4]
        )
        context["featured_authors"] = (
            User.objects.filter(articles__status=Article.Status.PUBLISHED)
            .annotate(
                published_total=Count(
                    "articles",
                    filter=Q(articles__status=Article.Status.PUBLISHED),
                    distinct=True,
                ),
                total_views=Sum("articles__views_count", default=0),
            )
            .order_by("-published_total", "-total_views", "username")[:4]
        )
        context["platform_metrics"] = [
            {"label": "Опубликованных статей", "value": published.count()},
            {"label": "Комментариев", "value": Comment.objects.filter(is_approved=True).count()},
            {"label": "Авторов", "value": User.objects.filter(role__in=[User.Roles.AUTHOR, User.Roles.ADMIN]).count()},
            {"label": "Тематик", "value": Category.objects.count()},
        ]
        context["categories"] = Category.objects.annotate(article_total=Count("articles")).order_by("-article_total", "name")[:8]
        context["tags"] = Tag.objects.annotate(article_total=Count("articles")).order_by("-article_total", "name")[:16]
        return context
