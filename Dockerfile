FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN mkdir /data
WORKDIR /app

RUN ln -s /data/conf/gunicorn.conf.py /app/gunicorn.conf.py

ADD pyproject.toml .
ADD uv.lock .

RUN uv sync --locked

ADD manage.py ./manage.py
ADD backend ./backend
ADD static ./static
ADD templates ./templates

RUN uv run manage.py collectstatic
RUN uv run manage.py migrate

CMD [ "uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "backend.wsgi" ]