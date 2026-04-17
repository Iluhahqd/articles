from dataclasses import dataclass


@dataclass
class PDFExportResult:
    filename: str
    content: bytes
    content_type: str = "application/pdf"


class ArticlePDFExporter:
    """
    Базовый каркас для дальнейшего PDF-экспорта одной статьи.
    При необходимости сюда можно подключить reportlab, weasyprint или wkhtmltopdf.
    """

    def export(self, article):
        raise NotImplementedError("PDF-экспорт еще не реализован, подготовлена только архитектура сервиса.")
