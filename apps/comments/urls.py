from django.urls import path

from apps.comments.views import CommentApproveToggleView, CommentCreateView, CommentDeleteView, CommentUpdateView


app_name = "comments"

urlpatterns = [
    path("create/<slug:slug>/", CommentCreateView.as_view(), name="create"),
    path("<int:pk>/edit/", CommentUpdateView.as_view(), name="edit"),
    path("<int:pk>/delete/", CommentDeleteView.as_view(), name="delete"),
    path("<int:pk>/approve/", CommentApproveToggleView.as_view(), name="approve"),
]
