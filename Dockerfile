FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -m benja

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=benja:benja . .

RUN mkdir -p /app/staticfiles /app/media \
    && chown -R benja:benja /app

USER benja

CMD [ "gunicorn", "expense.wsgi:application", "--bind", "0.0.0.0:8000"]