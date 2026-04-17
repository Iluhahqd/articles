from django.db.models import Count, Sum

from apps.articles.models import Article
from apps.users.models import User


def dashboard_statistics():
    published = Article.objects.published().with_engagement()
    return {
        "articles_total": Article.objects.count(),
        "published_total": published.count(),
        "draft_total": Article.objects.filter(status=Article.Status.DRAFT).count(),
        "authors_total": User.objects.filter(role__in=[User.Roles.AUTHOR, User.Roles.ADMIN]).count(),
        "top_articles": published.order_by("-rating", "-views_count")[:5],
        "most_discussed": published.order_by("-comments_count", "-published_at")[:5],
        "top_authors": (
            User.objects.annotate(
                articles_total=Count("articles"),
                total_views=Sum("articles__views_count", default=0),
            )
            .filter(articles_total__gt=0)
            .order_by("-articles_total", "-total_views")[:5]
        ),
    }
