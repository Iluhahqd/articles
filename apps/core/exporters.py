import csv
import zipfile
from io import BytesIO, StringIO

from django.db.models import Count
from django.http import HttpResponse
from django.utils import timezone

from apps.articles.models import Article, Favorite, Vote
from apps.comments.models import Comment
from apps.users.models import User


CSV_CONTENT_TYPE = "text/csv; charset=utf-8"
ZIP_CONTENT_TYPE = "application/zip"


def _format_datetime(value):
    if not value:
        return ""
    return timezone.localtime(value).strftime("%Y-%m-%d %H:%M:%S")


def _build_csv(headers, rows):
    buffer = StringIO()
    buffer.write("\ufeff")
    writer = csv.writer(buffer)
    writer.writerow(headers)
    writer.writerows(rows)
    return buffer.getvalue()


def csv_response(filename, headers, rows):
    response = HttpResponse(_build_csv(headers, rows), content_type=CSV_CONTENT_TYPE)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


def articles_export_data():
    headers = [
        "ID",
        "Title",
        "Author",
        "Status",
        "Category",
        "Tags",
        "Created At",
        "Published At",
        "Views",
        "Rating",
        "Comments",
        "Favorites",
    ]
    articles = (
        Article.objects.with_engagement()
        .select_related("author", "category")
        .prefetch_related("tags")
        .order_by("-created_at")
    )
    rows = (
        [
            article.id,
            article.title,
            article.author.username,
            article.get_status_display(),
            article.category.name if article.category else "",
            ", ".join(tag.name for tag in article.tags.all()),
            _format_datetime(article.created_at),
            _format_datetime(article.published_at),
            article.views_count,
            article.rating or 0,
            article.comments_count or 0,
            article.favorites_count or 0,
        ]
        for article in articles
    )
    return headers, rows


def users_export_data():
    headers = [
        "ID",
        "Username",
        "Email",
        "Role",
        "Is Staff",
        "Is Superuser",
        "Date Joined",
        "Articles",
        "Comments",
        "Favorites",
        "Votes",
    ]
    users = (
        User.objects.annotate(
            articles_total=Count("articles", distinct=True),
            comments_total=Count("comments", distinct=True),
            favorites_total=Count("favorite_articles", distinct=True),
            votes_total=Count("votes", distinct=True),
        )
        .order_by("-date_joined")
    )
    rows = (
        [
            user.id,
            user.username,
            user.email,
            user.get_role_display(),
            user.is_staff,
            user.is_superuser,
            _format_datetime(user.date_joined),
            user.articles_total,
            user.comments_total,
            user.favorites_total,
            user.votes_total,
        ]
        for user in users
    )
    return headers, rows


def comments_export_data():
    headers = [
        "ID",
        "Article ID",
        "Article",
        "Author",
        "Text",
        "Approved",
        "Created At",
        "Updated At",
    ]
    comments = Comment.objects.select_related("article", "author").order_by("-created_at")
    rows = (
        [
            comment.id,
            comment.article_id,
            comment.article.title,
            comment.author.username,
            comment.text,
            comment.is_approved,
            _format_datetime(comment.created_at),
            _format_datetime(comment.updated_at),
        ]
        for comment in comments
    )
    return headers, rows


def favorites_export_data():
    headers = ["ID", "User", "Article ID", "Article", "Created At"]
    favorites = Favorite.objects.select_related("user", "article").order_by("-created_at")
    rows = (
        [
            favorite.id,
            favorite.user.username,
            favorite.article_id,
            favorite.article.title,
            _format_datetime(favorite.created_at),
        ]
        for favorite in favorites
    )
    return headers, rows


def votes_export_data():
    headers = ["ID", "User", "Article ID", "Article", "Value", "Created At"]
    votes = Vote.objects.select_related("user", "article").order_by("-created_at")
    rows = (
        [
            vote.id,
            vote.user.username,
            vote.article_id,
            vote.article.title,
            vote.value,
            _format_datetime(vote.created_at),
        ]
        for vote in votes
    )
    return headers, rows


EXPORTS = {
    "articles": ("articles_export.csv", articles_export_data),
    "users": ("users_export.csv", users_export_data),
    "comments": ("comments_export.csv", comments_export_data),
    "favorites": ("favorites_export.csv", favorites_export_data),
    "votes": ("votes_export.csv", votes_export_data),
}


def export_dataset_response(dataset):
    filename, builder = EXPORTS[dataset]
    headers, rows = builder()
    return csv_response(filename, headers, rows)


def export_all_zip_response():
    archive = BytesIO()
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zip_file:
        for filename, builder in EXPORTS.values():
            headers, rows = builder()
            zip_file.writestr(filename, _build_csv(headers, rows).encode("utf-8"))

    response = HttpResponse(archive.getvalue(), content_type=ZIP_CONTENT_TYPE)
    response["Content-Disposition"] = 'attachment; filename="articlehub_export.zip"'
    return response
