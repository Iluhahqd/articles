from apps.articles.models import Category, Tag


def site_context(request):
    return {
        "nav_categories": Category.objects.order_by("name")[:8],
        "nav_tags": Tag.objects.order_by("name")[:12],
    }
