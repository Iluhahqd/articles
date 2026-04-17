from django import forms

from apps.comments.models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("text",)
        widgets = {
            "text": forms.Textarea(attrs={"rows": 4, "placeholder": "Поделитесь мнением о статье"}),
        }
        labels = {
            "text": "Комментарий",
        }
