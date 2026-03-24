```markdown
# Sentiment Analysis API

Микросервис для анализа тональности текста на русском языке с использованием модели RuBERT от Hugging Face. API сохраняет историю запросов в PostgreSQL и предоставляет статистику.

## 📋 Содержание

- [Возможности](#-возможности)
- [Технологии](#-технологии)
- [Требования](#-требования)
- [Установка и запуск](#-установка-и-запуск)
- [Использование API](#-использование-api)
- [Примеры запросов](#-примеры-запросов)
- [Структура проекта](#-структура-проекта)
- [Ответы API](#-ответы-api)
- [Возможные ошибки](#-возможные-ошибки)
- [Планы по улучшению](#-планы-по-улучшению)
- [Лицензия](#-лицензия)
- [Автор](#-автор)

## 🚀 Возможности

- ✅ Анализ тональности текста (POSITIVE / NEUTRAL / NEGATIVE)
- ✅ Сохранение всех запросов в PostgreSQL
- ✅ История запросов с пагинацией (limit/skip)
- ✅ Статистика по проанализированным текстам
- ✅ Docker Compose для простого развертывания
- ✅ Интерактивная документация FastAPI (Swagger UI)

## 🛠 Технологии

| Технология | Описание |
|------------|----------|
| **FastAPI** | Современный веб-фреймворк для Python |
| **Transformers** | Библиотека Hugging Face для работы с ML моделями |
| **RuBERT** | Модель для анализа тональности русского текста |
| **PostgreSQL** | Реляционная база данных |
| **SQLAlchemy** | ORM для работы с БД |
| **Docker / Docker Compose** | Контейнеризация и оркестрация |

## 📋 Требования

- **Docker Desktop** (версия 20.10+) или Docker Engine + Docker Compose
- **4 GB RAM** (рекомендуется для работы модели)
- **Свободные порты:** `8000` (API), `5432` (PostgreSQL)

## 📦 Установка и запуск

### Способ 1: Docker (рекомендуемый)

```bash
# 1. Клонируем репозиторий
git clone https://github.com/ВАШ_ЛОГИН/sentiment-analysis-api.git
cd sentiment-analysis-api

# 2. Запускаем проект
docker-compose up --build
```

После успешного запуска:

- API доступен: http://localhost:8000
- Документация: http://localhost:8000/docs
- PostgreSQL: localhost:5432 (логин: postgres, пароль: password)

### Способ 2: Локальный запуск (без Docker)

```bash
# 1. Создаем виртуальное окружение
python -m venv venv

# 2. Активируем его
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 3. Устанавливаем зависимости
pip install -r requirements.txt

# 4. Устанавливаем PostgreSQL и создаем базу данных
# Создайте базу данных с именем sentiment_db

# 5. Устанавливаем переменную окружения
# Linux/Mac:
export DATABASE_URL=postgresql://postgres:password@localhost:5432/sentiment_db
# Windows:
set DATABASE_URL=postgresql://postgres:password@localhost:5432/sentiment_db

# 6. Запускаем приложение
uvicorn main:app --reload
```

## 📡 Использование API

### POST /analyze

Анализирует тональность текста и сохраняет результат в базу данных.

**Параметры запроса:**

| Поле | Тип | Обязательное | Описание | Пример |
|------|-----|--------------|----------|--------|
| `text` | string | ✅ | Текст для анализа | "Я люблю Python" |
| `language` | string | ❌ | Язык текста (по умолчанию "ru") | "ru" |

**Пример запроса:**

```json
{
  "text": "Этот фильм просто потрясающий!",
  "language": "ru"
}
```

### GET /history

Возвращает историю запросов с пагинацией.

**Параметры:**

| Параметр | Тип | По умолчанию | Описание |
|----------|-----|--------------|----------|
| `limit` | int | 10 | Количество записей |
| `skip` | int | 0 | Сколько записей пропустить |

**Пример:** `/history?limit=5&skip=0`

### GET /stats

Возвращает общую статистику по всем запросам.

**Без параметров.**

### GET /docs

Интерактивная документация Swagger UI. Открой в браузере.

## 🧪 Примеры запросов

### cURL

```bash
# Анализ позитивного текста
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Я обожаю программировать!", "language": "ru"}'

# Анализ негативного текста
curl -X POST "http://localhost:8000/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "Это ужасно, ничего не работает", "language": "ru"}'

# Получить историю (последние 5 запросов)
curl "http://localhost:8000/history?limit=5"

# Получить статистику
curl "http://localhost:8000/stats"
```

### Python

```python
import requests

# URL вашего API
url = "http://localhost:8000/analyze"

# Данные для отправки
data = {
    "text": "Сегодня отличный день!",
    "language": "ru"
}

# Отправляем запрос
response = requests.post(url, json=data)

# Выводим результат
print(response.json())
```

### JavaScript (fetch)

```javascript
fetch('http://localhost:8000/analyze', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
    },
    body: JSON.stringify({
        text: 'JavaScript тоже крутой!',
        language: 'ru'
    })
})
.then(response => response.json())
.then(data => console.log(data));
```

## 📁 Структура проекта

```
sentiment-analysis-api/
│
├── main.py              # FastAPI приложение, все эндпоинты
├── models.py            # SQLAlchemy модели (структура таблиц)
├── database.py          # Подключение к БД, управление сессиями
│
├── Dockerfile           # Инструкция для сборки Docker образа
├── docker-compose.yml   # Оркестрация: API + PostgreSQL
├── requirements.txt     # Все Python зависимости
│
├── .dockerignore        # Файлы, которые НЕ попадают в Docker образ
├── .gitignore          # Файлы, которые НЕ попадают в Git
│
├── LICENSE             # Лицензия MIT
└── README.md           # Эта документация
```

## 📤 Ответы API

### POST /analyze — Успешный ответ (200)

```json
{
  "id": 1,
  "text": "Я обожаю программировать!",
  "sentiment": "POSITIVE",
  "confidence": 0.954,
  "language": "ru",
  "timestamp": "2024-03-24T12:00:00"
}
```

### POST /analyze — Ошибка валидации (422)

```json
{
  "detail": [
    {
      "loc": ["body", "text"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### GET /history — Успешный ответ (200)

```json
[
  {
    "id": 3,
    "text": "Я обожаю программировать!",
    "sentiment": "POSITIVE",
    "confidence": 0.95,
    "language": "ru",
    "timestamp": "2024-03-24T12:02:00"
  },
  {
    "id": 2,
    "text": "Это ужасно",
    "sentiment": "NEGATIVE",
    "confidence": 0.89,
    "language": "ru",
    "timestamp": "2024-03-24T12:01:00"
  }
]
```

### GET /stats — Успешный ответ (200)

```json
{
  "total_requests": 42,
  "sentiment_distribution": {
    "POSITIVE": 25,
    "NEUTRAL": 10,
    "NEGATIVE": 7
  },
  "last_request": "2024-03-24T12:02:00"
}
```

## ⚠️ Возможные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `Cannot connect to database` | PostgreSQL не запущен | Проверь: `docker-compose logs db` |
| `Port 8000 is already in use` | Порт занят другим процессом | Останови другой процесс или смени порт |
| `Model not loading` | Проблемы с сетью | Добавь зеркало PyPI в Dockerfile |
| `No module named 'torch'` | Не установлена зависимость | `pip install torch` |
| `psycopg2.OperationalError` | Неправильный DATABASE_URL | Убедись, что используешь `db` вместо `localhost` в Docker |

## 🔮 Планы по улучшению

- [ ] Поддержка английского языка
- [ ] Кэширование результатов (Redis)
- [ ] Асинхронная обработка тяжелых запросов
- [ ] Unit и интеграционные тесты (pytest)
- [ ] CI/CD через GitHub Actions
- [ ] Деплой на VPS или Render
- [ ] WebSocket для real-time анализа
- [ ] Docker image в Docker Hub
- [ ] Добавить больше моделей для выбора

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее в файле [LICENSE](LICENSE).

## 👨‍💻 Автор

**Егор**

- GitHub: [@GorkaEgor4kas](https://github.com/GorkaEgor4kas)
- Email [gorkaegor4kas@gmail.com]
---

⭐ Если этот проект был полезен, поставь звезду на GitHub!
```


