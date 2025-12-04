# Support Service - REST API

REST API сервис для User Support Assistant. Позволяет боту и другим приложениям получать ответы на вопросы через HTTP запросы.

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Вариант 1: Виртуальное окружение (рекомендуется)
python3 -m venv venv
source venv/bin/activate
pip install Flask flask-cors

# Вариант 2: Глобальная установка
pip3 install Flask flask-cors --break-system-packages
```

### 2. Индексация документации (если еще не сделано)

```bash
python3 support_assistant.py index
```

### 3. Запуск сервиса

```bash
# Через скрипт (проверяет зависимости)
./start_service.sh

# Или напрямую
python3 support_service.py

# С параметрами
python3 support_service.py --host 0.0.0.0 --port 8080 --debug
```

Сервис будет доступен на `http://localhost:5001`

### 4. Тестирование

В другом терминале:
```bash
python3 test_service.py test
```

## 📡 API Endpoints

### Основные

#### `GET /health`
Проверка работоспособности сервиса

**Response:**
```json
{
  "status": "ok",
  "service": "Movike Support Assistant",
  "version": "1.0.0"
}
```

#### `GET /api/stats`
Статистика системы

**Response:**
```json
{
  "users_count": 2,
  "tickets_count": 3,
  "documentation_chunks": 44
}
```

### Работа с вопросами

#### `POST /api/support/ask`
Главный endpoint для задания вопросов ассистенту

**Request:**
```json
{
  "question": "Почему не работает авторизация?",
  "email": "ivan.petrov@example.com"  // опционально
}
```

**Response:**
```json
{
  "question": "Почему не работает авторизация?",
  "answer": "📚 ИЗ ДОКУМЕНТАЦИИ:\n...",
  "sources": {
    "documentation": [
      {
        "file": "project/docs/SUPPORT_FAQ.md",
        "chunk_index": 0,
        "content": "...",
        "score": 10
      }
    ],
    "user_context": {
      "user_id": "user_001",
      "email": "ivan.petrov@example.com",
      "name": "Иван Петров",
      "subscription": "premium",
      "device": "Samsung Galaxy S21, Android 13",
      "app_version": "2.3.1"
    },
    "related_tickets": [
      {
        "ticket_id": "TICK-001",
        "subject": "Не работает авторизация",
        "status": "in_progress",
        "priority": "high",
        "context": {
          "error_code": "AUTH_001",
          "failed_attempts": 5
        }
      }
    ]
  },
  "confidence": "high"
}
```

**Примеры использования:**

```bash
# С пользователем
curl -X POST http://localhost:5001/api/support/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Почему не работает авторизация?", "email": "ivan.petrov@example.com"}'

# Без пользователя
curl -X POST http://localhost:5001/api/support/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Как восстановить пароль?"}'
```

### Работа с пользователями

#### `GET /api/users/<email>`
Получить информацию о пользователе

**Example:**
```bash
curl http://localhost:5001/api/users/ivan.petrov@example.com
```

**Response:**
```json
{
  "user_id": "user_001",
  "email": "ivan.petrov@example.com",
  "name": "Иван Петров",
  "subscription": "premium",
  "device": "Samsung Galaxy S21, Android 13",
  "app_version": "2.3.1"
}
```

#### `GET /api/users/<user_id>/tickets`
Получить все тикеты пользователя

**Example:**
```bash
curl http://localhost:5001/api/users/user_001/tickets
```

**Response:**
```json
{
  "user_id": "user_001",
  "tickets": [...],
  "count": 2
}
```

### Работа с тикетами

#### `GET /api/tickets/<ticket_id>`
Получить детали тикета

**Example:**
```bash
curl http://localhost:5001/api/tickets/TICK-001
```

**Response:**
```json
{
  "ticket": {
    "ticket_id": "TICK-001",
    "user_id": "user_001",
    "subject": "Не работает авторизация",
    "description": "...",
    "status": "in_progress",
    "priority": "high",
    "context": {
      "error_code": "AUTH_001",
      "failed_attempts": 5
    }
  },
  "user": {
    "user_id": "user_001",
    "name": "Иван Петров",
    ...
  }
}
```

#### `POST /api/tickets/search`
Поиск тикетов по ключевым словам

**Request:**
```json
{
  "keyword": "авторизация"
}
```

**Response:**
```json
{
  "keyword": "авторизация",
  "tickets": [...],
  "count": 1
}
```

### Работа с документацией

#### `POST /api/documentation/search`
Поиск в документации через RAG

**Request:**
```json
{
  "query": "как восстановить пароль",
  "limit": 5  // опционально, default 3
}
```

**Response:**
```json
{
  "query": "как восстановить пароль",
  "results": [
    {
      "file": "project/docs/SUPPORT_FAQ.md",
      "chunk_index": 1,
      "content": "### Как восстановить пароль?\n\n1. На экране входа нажмите...",
      "score": 8
    }
  ],
  "count": 1
}
```

## 🤖 Интеграция с ботом

### Telegram Bot пример

```python
import telebot
import requests

bot = telebot.TeleBot('YOUR_TOKEN')
API_URL = 'http://localhost:5001'

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот поддержки Movike. Задайте ваш вопрос.")

@bot.message_handler(func=lambda message: True)
def handle_question(message):
    # Отправляем вопрос в Support Service
    response = requests.post(
        f'{API_URL}/api/support/ask',
        json={'question': message.text},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        data = response.json()
        # Отправляем ответ пользователю
        bot.reply_to(message, data['answer'])

        # Показываем уверенность
        confidence_emoji = {
            'high': '✅',
            'medium': '⚠️',
            'low': '❓'
        }
        emoji = confidence_emoji.get(data['confidence'], '❓')
        bot.send_message(
            message.chat.id,
            f"{emoji} Уверенность: {data['confidence']}"
        )
    else:
        bot.reply_to(message, "Извините, произошла ошибка.")

bot.polling()
```

### Discord Bot пример

```python
import discord
import requests
from discord.ext import commands

bot = commands.Bot(command_prefix='!')
API_URL = 'http://localhost:5001'

@bot.event
async def on_ready():
    print(f'Bot {bot.user} запущен')

@bot.command(name='ask')
async def ask_support(ctx, *, question):
    """Задать вопрос поддержке: !ask Почему не работает авторизация?"""

    # Отправляем вопрос в Support Service
    response = requests.post(
        f'{API_URL}/api/support/ask',
        json={'question': question},
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        data = response.json()

        # Создаем embed сообщение
        embed = discord.Embed(
            title="🎬 Movike Support",
            description=data['answer'][:2000],  # Discord limit
            color=discord.Color.blue()
        )

        embed.add_field(
            name="Уверенность",
            value=data['confidence'],
            inline=True
        )

        if data['sources'].get('user_context'):
            user = data['sources']['user_context']
            embed.add_field(
                name="Пользователь",
                value=f"{user['name']} ({user['subscription']})",
                inline=True
            )

        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ Произошла ошибка при обработке запроса")

bot.run('YOUR_TOKEN')
```

### Python requests пример

```python
import requests
import json

API_URL = 'http://localhost:5001'

def ask_question(question, email=None):
    """Задать вопрос через API"""
    data = {'question': question}
    if email:
        data['email'] = email

    response = requests.post(
        f'{API_URL}/api/support/ask',
        json=data,
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API Error: {response.status_code}")

# Использование
result = ask_question("Как восстановить пароль?")
print(result['answer'])

# С контекстом пользователя
result = ask_question(
    "Почему не работает авторизация?",
    email="ivan.petrov@example.com"
)
print(f"Уверенность: {result['confidence']}")
print(result['answer'])
```

### JavaScript/Node.js пример

```javascript
const axios = require('axios');

const API_URL = 'http://localhost:5001';

async function askQuestion(question, email = null) {
    const data = { question };
    if (email) data.email = email;

    try {
        const response = await axios.post(
            `${API_URL}/api/support/ask`,
            data,
            {
                headers: { 'Content-Type': 'application/json' }
            }
        );

        return response.data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// Использование
(async () => {
    const result = await askQuestion("Как восстановить пароль?");
    console.log('Ответ:', result.answer);
    console.log('Уверенность:', result.confidence);
})();
```

## 🔧 Настройка

### Параметры запуска

```bash
python3 support_service.py --help
```

Доступные параметры:
- `--host` - хост для запуска (default: 0.0.0.0)
- `--port` - порт для запуска (default: 5001)
- `--debug` - режим отладки

### Запуск в production

Для production рекомендуется использовать gunicorn:

```bash
# Установка gunicorn
pip install gunicorn

# Запуск с 4 worker'ами
gunicorn -w 4 -b 0.0.0.0:5001 support_service:app

# С gevent для асинхронности
gunicorn -k gevent -w 4 -b 0.0.0.0:5001 support_service:app
```

### Docker

Создайте `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Индексация документации при сборке
RUN python3 support_assistant.py index

EXPOSE 5001

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5001", "support_service:app"]
```

Запуск:
```bash
docker build -t movike-support-service .
docker run -p 5001:5001 movike-support-service
```

## 📊 Мониторинг

### Health check

```bash
# Простая проверка
curl http://localhost:5001/health

# С интервалом (каждые 30 секунд)
watch -n 30 curl -s http://localhost:5001/health
```

### Логирование

Сервис выводит логи в stderr:
```bash
# Запуск с логированием в файл
python3 support_service.py 2>&1 | tee service.log

# Просмотр логов в реальном времени
tail -f service.log
```

## 🔐 Безопасность

### CORS

По умолчанию CORS разрешен для всех доменов. Для production настройте:

```python
# В support_service.py
from flask_cors import CORS

CORS(app, resources={
    r"/api/*": {
        "origins": ["https://yourdomain.com"]
    }
})
```

### Rate limiting

Для защиты от злоупотреблений добавьте rate limiting:

```bash
pip install Flask-Limiter
```

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/api/support/ask')
@limiter.limit("10 per minute")
def ask_question():
    ...
```

## 🧪 Тестирование

### Автоматический тест

```bash
# Запустите сервис в одном терминале
python3 support_service.py

# В другом терминале запустите тесты
python3 test_service.py test
```

### Ручное тестирование

```bash
# Health check
curl http://localhost:5001/health

# Вопрос без контекста
curl -X POST http://localhost:5001/api/support/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Как восстановить пароль?"}'

# Вопрос с контекстом
curl -X POST http://localhost:5001/api/support/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Почему не работает авторизация?", "email": "ivan.petrov@example.com"}'

# Поиск в документации
curl -X POST http://localhost:5001/api/documentation/search \
  -H "Content-Type: application/json" \
  -d '{"query": "подписка", "limit": 3}'
```

## 📝 Примеры ответов

### Успешный ответ с контекстом

```json
{
  "question": "Почему не работает авторизация?",
  "answer": "📚 ИЗ ДОКУМЕНТАЦИИ:\n\n1. Возможные причины:\n   - Неверные учетные данные\n   - Проблемы с сетью\n   ...\n\n👤 ВАШИ ДАННЫЕ:\n   Имя: Иван Петров\n   Подписка: premium\n   ...\n\n🎫 ПОХОЖИЕ ОБРАЩЕНИЯ:\n• TICK-001: Не работает авторизация\n  Статус: in_progress\n  Контекст: AUTH_001, 5 попыток",
  "sources": {
    "documentation": [...],
    "user_context": {...},
    "related_tickets": [...]
  },
  "confidence": "high"
}
```

### Ошибка 400 (Bad Request)

```json
{
  "error": "Missing required field: question"
}
```

### Ошибка 404 (Not Found)

```json
{
  "error": "User not found"
}
```

## 📚 Дополнительно

- Полная документация: `SUPPORT_ASSISTANT_README.md`
- Быстрый старт: `QUICK_START.md`
- Итоговый отчет: `SUPPORT_ASSISTANT_SUMMARY.md`

## ✅ Готово!

Теперь у вас есть REST API сервис, который может:
- ✅ Отвечать на вопросы через HTTP
- ✅ Интегрироваться с любыми ботами (Telegram, Discord, Slack)
- ✅ Работать с внешними приложениями
- ✅ Масштабироваться с gunicorn
- ✅ Деплоиться в Docker

**Начните с:**
```bash
./start_service.sh
```

Затем в другом терминале:
```bash
python3 test_service.py test
```
