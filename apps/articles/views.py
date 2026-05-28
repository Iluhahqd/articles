from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from apps.articles.forms import ArticleForm
from apps.articles.models import Article, Category, Favorite, Tag, Vote
from apps.comments.forms import CommentForm
from apps.comments.models import Comment
from apps.core.exporters import articles_export_data, csv_response
from apps.core.mixins import AuthorOrAdminRequiredMixin, RoleRequiredMixin
from apps.users.models import User


class FilteredArticleListMixin:
    paginate_by = 9

    def get_queryset(self):
        queryset = (
            Article.objects.published()
            .with_engagement()
            .select_related("author", "category")
            .prefetch_related("tags")
        )
        query = self.request.GET.get("query", "").strip()
        category = self.request.GET.get("category", "").strip()
        tag = self.request.GET.get("tag", "").strip()
        author = self.request.GET.get("author", "").strip()
        sort = self.request.GET.get("sort", "newest")

        queryset = queryset.searchable(query)
        if category:
            queryset = queryset.filter(category__slug=category)
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        if author:
            queryset = queryset.filter(author__username=author)

        ordering_map = {
            "newest": ("-published_at", "-created_at"),
            "oldest": ("published_at", "created_at"),
            "rating": ("-rating", "-published_at"),
            "comments": ("-comments_count", "-published_at"),
            "views": ("-views_count", "-published_at"),
        }
        return queryset.distinct().order_by(*ordering_map.get(sort, ordering_map["newest"]))


class FavoriteContextMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["favorite_article_ids"] = set()
        if user.is_authenticated:
            articles = context.get("articles") or context.get("object_list") or []
            article_ids = [article.pk for article in articles]
            context["favorite_article_ids"] = set(
                Favorite.objects.filter(user=user, article_id__in=article_ids).values_list("article_id", flat=True)
            )
        return context


class ArticleListView(FavoriteContextMixin, FilteredArticleListMixin, ListView):
    model = Article
    template_name = "articles/article_list.html"
    context_object_name = "articles"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = "Все статьи"
        context["categories"] = Category.objects.order_by("name")
        context["tags"] = Tag.objects.order_by("name")
        return context


class CategoryDetailView(ArticleListView):
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        queryset = super().get_queryset()
        return queryset.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Категория: {self.category.name}"
        context["category_object"] = self.category
        return context


class TagDetailView(ArticleListView):
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        queryset = super().get_queryset()
        return queryset.filter(tags=self.tag)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Тег: {self.tag.name}"
        context["tag_object"] = self.tag
        return context


class AuthorDetailView(ArticleListView):
    def get_queryset(self):
        self.author_object = get_object_or_404(User, username=self.kwargs["username"])
        queryset = super().get_queryset()
        return queryset.filter(author=self.author_object)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = f"Автор: {self.author_object.username}"
        context["author_object"] = self.author_object
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = "articles/article_detail.html"
    context_object_name = "article"
    slug_field = "slug"

    def get_queryset(self):
        queryset = Article.objects.with_engagement().select_related("author", "category").prefetch_related("tags")
        user = self.request.user
        if user.is_authenticated and user.is_admin:
            return queryset
        if user.is_authenticated:
            return queryset.filter(Q(status=Article.Status.PUBLISHED) | Q(author=user)).distinct()
        return queryset.published()

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        Article.objects.filter(pk=self.object.pk).update(views_count=F("views_count") + 1)
        self.object.refresh_from_db(fields=["views_count"])
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        context["comment_form"] = CommentForm()
        comments_queryset = article.comments.select_related("author")
        if not self.request.user.is_authenticated or not self.request.user.is_admin:
            comments_queryset = comments_queryset.filter(is_approved=True)
        context["comments"] = comments_queryset
        context["related_articles"] = (
            Article.objects.published()
            .with_engagement()
            .filter(category=article.category)
            .exclude(pk=article.pk)
            .select_related("author", "category")[:4]
        )
        if self.request.user.is_authenticated:
            context["user_vote"] = Vote.objects.filter(article=article, user=self.request.user).first()
            context["is_favorite"] = Favorite.objects.filter(article=article, user=self.request.user).exists()
        return context


class ArticleCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = (User.Roles.AUTHOR, User.Roles.ADMIN)
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Статья создана.")
        return super().form_valid(form)


class ArticleUpdateView(AuthorOrAdminRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "articles/article_form.html"
    slug_field = "slug"

    def form_valid(self, form):
        messages.success(self.request, "Статья обновлена.")
        return super().form_valid(form)


class ArticleDeleteView(AuthorOrAdminRequiredMixin, DeleteView):
    model = Article
    template_name = "articles/article_confirm_delete.html"
    success_url = reverse_lazy("articles:mine")
    slug_field = "slug"

    def form_valid(self, form):
        messages.success(self.request, "Статья удалена.")
        return super().form_valid(form)


class MyArticleListView(RoleRequiredMixin, ListView):
    allowed_roles = (User.Roles.AUTHOR, User.Roles.ADMIN)
    model = Article
    template_name = "articles/my_articles.html"
    context_object_name = "articles"
    paginate_by = 10

    def get_queryset(self):
        queryset = Article.objects.with_engagement().select_related("category")
        if self.request.user.is_admin:
            return queryset.order_by("-updated_at")
        return queryset.filter(author=self.request.user).order_by("-updated_at")


class FavoriteListView(FavoriteContextMixin, LoginRequiredMixin, ListView):
    template_name = "articles/favorites.html"
    context_object_name = "articles"
    paginate_by = 9

    def get_queryset(self):
        return (
            Article.objects.published()
            .with_engagement()
            .filter(favorited_by__user=self.request.user)
            .select_related("author", "category")
            .prefetch_related("tags")
            .order_by("-favorited_by__created_at")
        )


class VoteToggleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)
        value = int(request.POST.get("value", "1"))
        if value not in (-1, 1):
            messages.error(request, "Некорректное значение голоса.")
            return redirect(article.get_absolute_url())

        vote, created = Vote.objects.get_or_create(article=article, user=request.user, defaults={"value": value})
        if not created:
            if vote.value == value:
                vote.delete()
                messages.info(request, "Ваш голос снят.")
            else:
                vote.value = value
                vote.save(update_fields=["value"])
                messages.success(request, "Ваш голос обновлен.")
        else:
            messages.success(request, "Ваш голос учтен.")
        return redirect(article.get_absolute_url())


class FavoriteToggleView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)
        favorite, created = Favorite.objects.get_or_create(article=article, user=request.user)
        if created:
            messages.success(request, "Статья добавлена в избранное.")
        else:
            favorite.delete()
            messages.info(request, "Статья удалена из избранного.")
        next_url = request.POST.get("next") or request.META.get("HTTP_REFERER")
        if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)
        return redirect(article.get_absolute_url())


def export_articles_csv(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        messages.error(request, "Экспорт доступен только администратору.")
        return redirect("users:login")

    headers, rows = articles_export_data()
    return csv_response("articles_export.csv", headers, rows)
