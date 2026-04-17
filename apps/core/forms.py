from django import forms


class ArticleFilterForm(forms.Form):
    query = forms.CharField(required=False, label="Поиск")
    category = forms.CharField(required=False, label="Категория")
    tag = forms.CharField(required=False, label="Тег")
    author = forms.CharField(required=False, label="Автор")
    sort = forms.ChoiceField(
        required=False,
        label="Сортировка",
        choices=(
            ("newest", "Сначала новые"),
            ("oldest", "Сначала старые"),
            ("rating", "По рейтингу"),
            ("comments", "По комментариям"),
            ("views", "По просмотрам"),
        ),
    )
