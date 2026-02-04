FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

ADD pyproject.toml .
ADD uv.lock .

RUN uv sync --locked

ADD manage.py ./manage.py
ADD backend ./backend
ADD static ./static
ADD templates ./templates

RUN uv run manage.py collectstatic

CMD [ "uv", "run", "gunicorn", "backend.wsgi" ]