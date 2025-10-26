## **Task Management API**

Простой REST API для управления задачами, построенный на FastAPI. Позволяет создавать, читать, обновлять и удалять задачи.

### **Описание проекта**

Этот проект предоставляет базовый CRUD (Create, Read, Update, Delete) API для управления задачами. Каждая задача содержит название и статус выполнения.

### **Основные возможности:**

- Получение списка всех задач

- Получение конкретной задачи по названию

- Создание новой задачи

- Обновление существующей задачи

- Удаление задачи

### **Технологии**

- **FastAPI** - современный, быстрый веб-фреймворк для построения API с Python

- **Pydantic** - валидация данных и сериализация

- **Uvicorn** - ASGI сервер для запуска приложения

### **Установка и запуск**

### **Предварительные требования**

- Python 3.7+

- pip (менеджер пакетов Python)

### **Шаги установки**

1\. Клонируйте репозиторий или создайте рабочую директорию:
```bash
mkdir task-api
cd task-api
```

2\. Создайте виртуальное окружение (рекомендуется):
``` bash
python -m venv venv
source venv/bin/activate  # для Linux/MacOS
# или
venv\Scripts\activate  # для Windows
```

3\. Установите зависимости:
```bash
pip install fastapi uvicorn
```

4\. Создайте файл ```main.py``` с кодом приложения

5\. Запустите сервер:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Сервер будет доступен по адресу: http://localhost:8000

## **Документация API**

После запуска сервера доступна автоматическая документация:

- Swagger UI: http://localhost:8000/docs

- ReDoc: http://localhost:8000/redoc

## **Примеры использования API**

1\. **Получить все задачи**

Запрос:

```bash
GET /tasks/
```
Ответ:

```json
[
  {
    "name": "Task 1",
    "status": true
  },
  {
    "name": "Task 2",
    "status": false
  }
]
```

2\. **Получить задачу по названию**
Запрос:

```bash
GET /tasks/important_task
```
Ответ (если задача найдена):

```json
{
  "name": "important_task",
  "status": false
}
```
Ответ (если задача не найдена):

```json
null
```

3\. **Создать новую задачу**
Запрос:

```bash
POST /tasks/
Content-Type: application/json

{
  "name": "new_task",
  "status": false
}
```
Ответ:

```json
{
  "name": "new_task",
  "status": false
}
```

4\. **Обновить задачу**
Запрос:

```bash
PATCH /tasks/
Content-Type: application/json

{
  "name": "existing_task",
  "status": true
}
```
Ответ:

```json
{}

5\. **Удалить задачу**
Запрос:

```bash
DELETE /tasks/task_to_delete
```
Ответ:
Статус 204 (No Content)

### Структура данных

### Модель Task
```json
{
  "name": "string",
  "status": "boolean"
}
```
Поля:

- _name_ (string, обязательный) - уникальное название задачи

- _status_ (_boolean_, обязательный) - статус выполнения задачи (_true_ - выполнена, _false_ - не выполнена)

## Примеры использования с curl

### Создание задачи

```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{"name": "learn_fastapi", "status": false}'
```

### Получение всех задач
```bash
curl -X GET "http://localhost:8000/tasks/"
```

### Получение конкретной задачи
```bash
curl -X GET "http://localhost:8000/tasks/learn_fastapi"
```

### Обновление задачи
```bash
curl -X PATCH "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{"name": "learn_fastapi", "status": true}'
```

### Удаление задачи
```bash
curl -X DELETE "http://localhost:8000/tasks/learn_fastapi"
```

### Обработка ошибок

API возвращает стандартные HTTP статусы:

- 200 - Успешный запрос

- 201 - Успешное создание

- 204 - Успешное удаление (нет содержимого)

- 422 - Ошибка валидации данных

При ошибках валидации возвращается детальная информация об ошибках в формате:

```json
{
  "detail": [
    {
      "loc": ["string", 0],
      "msg": "string",
      "type": "string"
    }
  ]
}
```

### Разработка

Для разработки рекомендуется использовать режим `--reload` при запуске uvicorn, который автоматически перезагружает сервер при изменениях кода:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```