FROM python:3.13

WORKDIR /app

# Устанавливаем uv
RUN pip install uv

# Копируем файлы зависимостей
COPY pyproject.toml ./

# Устанавливаем зависимости с помощью uv
RUN uv pip install --system -r pyproject.toml

# Копируем исходный код
COPY . .

# Открываем порт
EXPOSE 8000

# Команда для запуска
CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]