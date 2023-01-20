FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV POETRY_VERSION=${POETRY_VERSION:-1.2.0}

ENV WORKERS=${WORKERS:-1}
ENV HOST=${HOST:-0.0.0.0}
ENV PORT=${PORT:-8000}

WORKDIR /opt

RUN apt-get update && apt-get install -y make

RUN pip install --upgrade pip && pip install poetry==$POETRY_VERSION

COPY poetry.lock pyproject.toml README.md ./

RUN poetry config virtualenvs.create false && poetry install --no-root --no-interaction --no-cache --without=dev

COPY suhrob_sub ./suhrob_sub

RUN poetry build -f wheel
RUN pip install dist/suhrob_sub-*.whl --no-deps
RUN rm -rf *

COPY makefile ./

ENTRYPOINT gunicorn suhrob_sub.suhrob.wsgi --workers $WORKERS --bind $HOST:$PORT