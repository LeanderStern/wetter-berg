FROM python:3.14-slim-trixie

ENV UV_NO_DEV=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# only needed when needing a specific local
RUN apt-get update && apt-get install -y locales \
    && sed -i '/de_DE.UTF-8/s/^# //g' /etc/locale.gen \
    && locale-gen de_DE.UTF-8 \
    && rm -rf /var/lib/apt/lists/*

COPY . /app

WORKDIR /app

RUN uv sync --locked

RUN chmod +x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["uv", "run", "main.py"]