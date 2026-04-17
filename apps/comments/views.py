from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, UpdateView

from apps.articles.models import Article
from apps.comments.forms import CommentForm
from apps.comments.models import Comment
from apps.core.mixins import AuthorOrAdminRequiredMixin


class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, slug):
        article = get_object_or_404(Article, slug=slug, status=Article.Status.PUBLISHED)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.is_approved = request.user.is_admin
            comment.save()
            if request.user.is_admin:
                messages.success(request, "Комментарий опубликован.")
            else:
                messages.success(request, "Комментарий отправлен на модерацию.")
        else:
            messages.error(request, "Не удалось сохранить комментарий.")
        return redirect(article.get_absolute_url())


class CommentUpdateView(AuthorOrAdminRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "comments/comment_form.html"

    def get_object_owner(self, obj):
        return obj.author

    def get_success_url(self):
        return self.object.article.get_absolute_url()

    def form_valid(self, form):
        if not self.request.user.is_admin:
            form.instance.is_approved = False
        messages.success(self.request, "Комментарий обновлен.")
        return super().form_valid(form)


class CommentDeleteView(AuthorOrAdminRequiredMixin, DeleteView):
    model = Comment
    template_name = "comments/comment_confirm_delete.html"

    def get_object_owner(self, obj):
        return obj.author

    def get_success_url(self):
        messages.success(self.request, "Комментарий удален.")
        return self.object.article.get_absolute_url()


class CommentApproveToggleView(LoginRequiredMixin, View):
    def post(self, request, pk):
        if not request.user.is_admin:
            messages.error(request, "У вас нет прав для модерации комментариев.")
            return redirect("core:home")

        comment = get_object_or_404(Comment, pk=pk)
        comment.is_approved = not comment.is_approved
        comment.save(update_fields=["is_approved"])
        messages.success(request, "Статус комментария обновлен.")
        return redirect(comment.article.get_absolute_url())
