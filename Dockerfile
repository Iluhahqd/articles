FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
COPY wheelhouse/ /wheelhouse/
RUN if [ -n "$(find /wheelhouse -name '*.whl' -print -quit)" ]; then \
        pip install --no-cache-dir --no-index --find-links=/wheelhouse -r requirements.txt; \
    else \
        pip install --no-cache-dir --timeout 120 -r requirements.txt; \
    fi

COPY . .

CMD ["sh", "/app/entrypoint.sh"]
