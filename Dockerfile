FROM python:3.12-slim-trixie
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --compile-bytecode --no-cache --no-dev

COPY src/ ./

EXPOSE 8000

COPY .env .

# Команда для запуска
CMD ["uv","run","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]