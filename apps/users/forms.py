from django import forms
from django.contrib.auth.forms import UserCreationForm

from apps.users.models import User


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].choices = [
            (User.Roles.USER, "Пользователь"),
            (User.Roles.AUTHOR, "Автор"),
        ]

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "role")
        labels = {
            "username": "Имя пользователя",
            "first_name": "Имя",
            "last_name": "Фамилия",
            "role": "Роль",
        }

    def clean_role(self):
        role = self.cleaned_data["role"]
        if role == User.Roles.ADMIN:
            return User.Roles.USER
        return role


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "avatar", "bio")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 4}),
        }
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "avatar": "Аватар",
            "bio": "О себе",
        }
