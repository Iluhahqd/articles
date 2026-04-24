from django import template
from django.utils.html import escape
from django.utils.safestring import mark_safe


register = template.Library()


@register.filter
def richtext(value):
    if not value:
        return ""

    blocks = []
    lines = [line.rstrip() for line in value.splitlines()]
    paragraph_buffer = []
    list_buffer = []

    def flush_paragraph():
        nonlocal paragraph_buffer
        if paragraph_buffer:
            text = " ".join(paragraph_buffer)
            blocks.append(f'<p class="article-paragraph">{escape(text)}</p>')
            paragraph_buffer = []

    def flush_list():
        nonlocal list_buffer
        if list_buffer:
            items = "".join(f"<li>{escape(item)}</li>" for item in list_buffer)
            blocks.append(f'<ul class="article-list">{items}</ul>')
            list_buffer = []

    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            flush_paragraph()
            flush_list()
            continue
        if line.startswith("## "):
            flush_paragraph()
            flush_list()
            blocks.append(f'<h2 class="article-heading">{escape(line[3:])}</h2>')
            continue
        if line.startswith("### "):
            flush_paragraph()
            flush_list()
            blocks.append(f'<h3 class="article-subheading">{escape(line[4:])}</h3>')
            continue
        if line.startswith("- "):
            flush_paragraph()
            list_buffer.append(line[2:])
            continue
        flush_list()
        paragraph_buffer.append(line)

    flush_paragraph()
    flush_list()
    return mark_safe("\n".join(blocks))
