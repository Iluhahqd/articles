from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("articles", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="cover_image_credit",
            field=models.CharField(blank=True, max_length=160, verbose_name="Автор фото"),
        ),
        migrations.AddField(
            model_name="article",
            name="cover_image_source_url",
            field=models.URLField(blank=True, verbose_name="Ссылка на источник фото"),
        ),
        migrations.AddField(
            model_name="article",
            name="cover_image_url",
            field=models.URLField(blank=True, verbose_name="Внешняя обложка"),
        ),
    ]
