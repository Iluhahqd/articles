from django.utils.text import slugify


def unique_slugify(instance, value, slug_field_name="slug"):
    slug_field = instance._meta.get_field(slug_field_name)
    base_slug = slugify(value)[: slug_field.max_length or 50] or "item"
    model_class = instance.__class__
    slug = base_slug
    suffix = 1

    while model_class.objects.filter(**{slug_field_name: slug}).exclude(pk=instance.pk).exists():
        slug = f"{base_slug[: max((slug_field.max_length or 50) - len(str(suffix)) - 1, 1)]}-{suffix}"
        suffix += 1

    setattr(instance, slug_field.attname, slug)
