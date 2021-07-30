FROM docker.io/library/python:slim

WORKDIR /app
COPY ./pyproject.toml pyproject.toml

RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y netcat \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root --no-dev

COPY . .

RUN python manage.py collectstatic --no-input

EXPOSE 8000/tcp
CMD python manage.py migrate && \
    gunicorn --bind 0.0.0.0:8000 stranger_parties.wsgi:application \
             --workers 2 \
             --preload \
             --log-file - \
             --log-level=debug \
             --error-logfile -
