from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    allowed_roles = ()
    message = "У вас недостаточно прав для выполнения этого действия."

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and (user.is_superuser or user.role in self.allowed_roles)

    def handle_no_permission(self):
        messages.error(self.request, self.message)
        if self.request.user.is_authenticated:
            return redirect("core:home")
        return redirect("users:login")


class AuthorOrAdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    message = "Вы можете управлять только собственными материалами."

    def get_object_owner(self, obj):
        return getattr(obj, "author", None)

    def test_func(self):
        user = self.request.user
        obj = self.get_object()
        owner = self.get_object_owner(obj)
        return user.is_authenticated and (user.is_superuser or user.is_admin or owner == user)

    def handle_no_permission(self):
        messages.error(self.request, self.message)
        return redirect("core:home")
