from django.urls import path

from apps.articles.views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
    AuthorDetailView,
    CategoryDetailView,
    FavoriteListView,
    FavoriteToggleView,
    MyArticleListView,
    TagDetailView,
    VoteToggleView,
    export_articles_csv,
)


app_name = "articles"

urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    path("mine/", MyArticleListView.as_view(), name="mine"),
    path("favorites/", FavoriteListView.as_view(), name="favorites"),
    path("create/", ArticleCreateView.as_view(), name="create"),
    path("export/csv/", export_articles_csv, name="export_csv"),
    path("category/<slug:slug>/", CategoryDetailView.as_view(), name="category_detail"),
    path("tag/<slug:slug>/", TagDetailView.as_view(), name="tag_detail"),
    path("author/<str:username>/", AuthorDetailView.as_view(), name="author_detail"),
    path("<slug:slug>/", ArticleDetailView.as_view(), name="detail"),
    path("<slug:slug>/edit/", ArticleUpdateView.as_view(), name="edit"),
    path("<slug:slug>/delete/", ArticleDeleteView.as_view(), name="delete"),
    path("<slug:slug>/vote/", VoteToggleView.as_view(), name="vote"),
    path("<slug:slug>/favorite/", FavoriteToggleView.as_view(), name="favorite"),
]
