from pathlib import Path
from urllib.parse import urlparse

from django.core.files.base import ContentFile
from django.utils.text import slugify
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


CONTENT_TYPE_EXTENSIONS = {
    "image/jpeg": ".jpg",
    "image/jpg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


def _guess_extension(url, content_type):
    if content_type:
        normalized = content_type.split(";")[0].strip().lower()
        if normalized in CONTENT_TYPE_EXTENSIONS:
            return CONTENT_TYPE_EXTENSIONS[normalized]

    path = urlparse(url).path
    suffix = Path(path).suffix.lower()
    if suffix in {".jpg", ".jpeg", ".png", ".webp"}:
        return ".jpg" if suffix == ".jpeg" else suffix
    return ".jpg"


def download_cover_to_article(article, timeout=20):
    if not article.cover_image_url or article.cover_image:
        return False, "skip"

    session = requests.Session()
    retry_strategy = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=1,
        status_forcelist=(429, 500, 502, 503, 504),
        allowed_methods=("GET",),
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    try:
        response = session.get(
            article.cover_image_url,
            timeout=timeout,
            headers={
                "User-Agent": "ArticleHubBot/1.0 (+https://articlehub.local)",
                "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
            },
            allow_redirects=True,
            stream=True,
        )
        response.raise_for_status()
        content = response.content
        if not content:
            return False, "empty"
        extension = _guess_extension(article.cover_image_url, response.headers.get("Content-Type"))
    except requests.RequestException as exc:
        return False, str(exc)
    finally:
        session.close()

    filename = f"{slugify(article.slug or article.title or 'article-cover')}{extension}"
    article.cover_image.save(filename, ContentFile(content), save=False)
    return True, filename
