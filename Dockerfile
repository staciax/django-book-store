ARG PYTHON_VERSION=3.12
FROM ghcr.io/astral-sh/uv:python${PYTHON_VERSION}-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

FROM python:${PYTHON_VERSION}-slim-bookworm

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
    
COPY --from=builder --chown=app:app /app /app
COPY --from=busybox:stable --chown=app:app /bin/nc /bin/nc

ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT ["./entrypoint.sh"]

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]