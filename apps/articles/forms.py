from django import forms

from apps.articles.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "short_description",
            "content",
            "cover_image",
            "status",
            "category",
            "tags",
        )
        widgets = {
            "content": forms.Textarea(attrs={"rows": 12}),
            "short_description": forms.Textarea(attrs={"rows": 3}),
            "tags": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "title": "Заголовок",
            "short_description": "Краткое описание",
            "content": "Текст статьи",
            "cover_image": "Обложка",
            "status": "Статус",
            "category": "Категория",
            "tags": "Теги",
        }
