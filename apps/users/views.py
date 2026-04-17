from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from apps.articles.models import Article
from apps.users.forms import UserRegisterForm
from apps.users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "account/register.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Регистрация прошла успешно.")
        return response


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users/profile.html"
    context_object_name = "profile_user"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        articles = Article.objects.filter(author=user).with_engagement()
        context["articles_total"] = articles.count()
        context["published_total"] = articles.filter(status=Article.Status.PUBLISHED).count()
        context["favorites_total"] = user.favorite_articles.count()
        context["recent_articles"] = articles[:5]
        context["author_rankings"] = (
            Article.objects.filter(author=user)
            .published()
            .aggregate(total_views=Sum("views_count", default=0))
        )
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "users/profile_edit.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Профиль обновлен.")
        return super().form_valid(form)
