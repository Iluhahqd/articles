from django import forms


class UserSearchForm(forms.Form):
    query = forms.CharField(required=False, label="Поиск пользователя")
