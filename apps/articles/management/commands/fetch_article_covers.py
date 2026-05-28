from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Команда оставлена для совместимости. В текущей версии используются только локальные встроенные обложки."

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.WARNING(
                "Внешние обложки отключены. Ничего скачивать не нужно: стартовые статьи используют локальные встроенные изображения."
            )
        )
