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
            "cover_image_url",
            "cover_image_credit",
            "cover_image_source_url",
            "status",
            "category",
            "tags",
        )
        widgets = {
            "content": forms.Textarea(attrs={"rows": 12}),
            "short_description": forms.Textarea(attrs={"rows": 3}),
            "cover_image_url": forms.URLInput(attrs={"placeholder": "https://images.unsplash.com/..."}),
            "cover_image_source_url": forms.URLInput(attrs={"placeholder": "https://unsplash.com/photos/..."}),
            "tags": forms.CheckboxSelectMultiple(),
        }
        labels = {
            "title": "Заголовок",
            "short_description": "Краткое описание",
            "content": "Текст статьи",
            "cover_image": "Обложка",
            "cover_image_url": "Внешняя обложка",
            "cover_image_credit": "Автор фото",
            "cover_image_source_url": "Ссылка на источник фото",
            "status": "Статус",
            "category": "Категория",
            "tags": "Теги",
        }
