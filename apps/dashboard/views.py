from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Sum
from django.http import Http404
from django.views import View
from django.views.generic import ListView, TemplateView

from apps.articles.models import Article, Category, Tag
from apps.articles.services import dashboard_statistics
from apps.comments.models import Comment
from apps.core.exporters import EXPORTS, export_all_zip_response, export_dataset_response
from apps.users.models import User


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin


class DashboardHomeView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(dashboard_statistics())
        context["recent_comments"] = Comment.objects.select_related("author", "article").order_by("-created_at")[:10]
        context["latest_users"] = User.objects.order_by("-date_joined")[:8]
        return context


class StatisticsView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["stats"] = dashboard_statistics()
        context["category_stats"] = Category.objects.annotate(total_articles=Count("articles")).order_by("-total_articles", "name")
        context["tag_stats"] = Tag.objects.annotate(total_articles=Count("articles")).order_by("-total_articles", "name")[:10]
        context["engagement_stats"] = (
            Article.objects.published()
            .with_engagement()
            .values("title", "views_count", "rating", "comments_count")
            .order_by("-views_count")[:10]
        )
        context["user_stats"] = (
            User.objects.annotate(
                articles_total=Count("articles"),
                comments_total=Count("comments"),
                votes_total=Count("votes"),
                total_views=Sum("articles__views_count", default=0),
            )
            .order_by("-articles_total", "-comments_total")[:10]
        )
        return context


class UserManagementView(AdminRequiredMixin, ListView):
    template_name = "dashboard/users.html"
    model = User
    context_object_name = "users"
    paginate_by = 20

    def get_queryset(self):
        queryset = User.objects.order_by("-date_joined")
        query = self.request.GET.get("query", "").strip()
        if query:
            queryset = queryset.filter(username__icontains=query)
        return queryset


class ExportView(AdminRequiredMixin, TemplateView):
    template_name = "dashboard/export.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["exports"] = (
            ("articles", "Статьи", "Публикации, статусы, категории, теги и метрики вовлеченности."),
            ("users", "Пользователи", "Аккаунты, роли и количество связанных действий."),
            ("comments", "Комментарии", "Тексты комментариев, авторы, статьи и статус модерации."),
            ("favorites", "Избранное", "Связи пользователей с сохраненными статьями."),
            ("votes", "Голоса", "Лайки и дизлайки пользователей по статьям."),
        )
        return context


class ExportDatasetView(AdminRequiredMixin, View):
    def get(self, request, dataset):
        if dataset not in EXPORTS:
            raise Http404("Набор данных не найден.")
        return export_dataset_response(dataset)


class ExportAllView(AdminRequiredMixin, View):
    def get(self, request):
        return export_all_zip_response()
