# Movike AI Assistants

Два AI-ассистента для работы с проектом Movike.

## 🎯 Два ассистента

### 1. Code Assistant - Помощь с кодом
Отвечает на вопросы о коде, архитектуре и документации проекта.

```bash
python3 code_assistant.py "Как использовать ApiService?"
```

### 2. Support Assistant - Техническая поддержка
Отвечает на вопросы пользователей о приложении, используя FAQ и CRM данные.

```bash
python3 support_assistant.py ask "Почему не работает авторизация?" user@email.com
```

## 📁 Структура файлов

```
assistant/
├── code_assistant.py          # Code Assistant (вопросы о коде)
├── support_assistant.py       # Support Assistant (техподдержка)
├── support_service.py         # REST API для Support Assistant
├── simple_rag.py              # RAG система (общая для обоих)
│
├── mcp_git_server.py          # MCP сервер для git
├── mcp_crm_server.py          # MCP сервер для CRM
├── code_reviewer.py           # Code reviewer
│
├── example_bot.py             # Пример бота
├── test_service.py            # Тестовый клиент API
│
├── crm_data.json              # Данные CRM (пользователи, тикеты)
├── rag_index.json             # RAG индекс (генерируется)
│
└── docs/
    ├── README.md              # Этот файл
    ├── QUICK_START.md         # Быстрый старт
    ├── HOW_TO_USE.md          # Подробное руководство
    ├── CODE_ASSISTANT_README.md    # Документация Code Assistant
    ├── SERVICE_README.md      # Документация REST API
    ├── SERVICE_SUMMARY.md     # Архитектура сервиса
    ├── INSTALL.md             # Установка зависимостей
    ├── QUICKREF.md            # Быстрая справка
    └── COMMANDS.md            # Команды
```

## 🚀 Быстрый старт

### Первый запуск (индексация)

```bash
# Индексация для Code Assistant
python3 code_assistant.py index

# Индексация для Support Assistant
python3 support_assistant.py index
```

### Code Assistant

```bash
# Интерактивный режим
python3 code_assistant.py

# Один вопрос
python3 code_assistant.py "Где находится FeedViewModel?"

# Поиск по коду
python3 code_assistant.py "ApiService"
```

### Support Assistant

```bash
# Интерактивный режим
python3 support_assistant.py

# Вопрос с контекстом пользователя
python3 support_assistant.py ask "Почему не работает авторизация?" ivan.petrov@example.com

# Вопрос без контекста
python3 support_assistant.py ask "Как восстановить пароль?"
```

### Support Service (REST API)

```bash
# Установка (создает venv и устанавливает Flask)
./setup_service.sh

# Запуск сервиса
source venv/bin/activate
python3 support_service.py

# Тест API
python3 test_service.py test

# Пример бота
python3 example_bot.py
```

## 📚 Документация

| Документ | Описание |
|----------|----------|
| **QUICK_START.md** | Быстрый старт - начните отсюда |
| **HOW_TO_USE.md** | Подробное руководство |
| **CODE_ASSISTANT_README.md** | Документация Code Assistant |
| **SERVICE_README.md** | REST API документация |
| **SERVICE_SUMMARY.md** | Архитектура и deployment |
| **INSTALL.md** | Установка Flask для REST API |
| **QUICKREF.md** | Быстрая справка по командам |
| **COMMANDS.md** | Все доступные команды |

## 💡 Примеры использования

### Вопросы о коде

```bash
python3 code_assistant.py "Как работает авторизация?"
python3 code_assistant.py "Где находится FeedViewModel?"
python3 code_assistant.py "ApiService"
```

### Вопросы техподдержки

```bash
python3 support_assistant.py ask "Почему не работает авторизация?" ivan.petrov@example.com
python3 support_assistant.py ask "Не прошел платеж"
python3 support_assistant.py ask "Как отменить подписку?"
```

### REST API (для ботов)

```bash
# Запуск сервиса
source venv/bin/activate
python3 support_service.py

# В другом терминале
curl -X POST http://localhost:5000/api/support/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Как восстановить пароль?"}'
```

## 🤖 Интеграция с ботом

```python
import requests

# Отправить вопрос в Support Service
response = requests.post(
    'http://localhost:5000/api/support/ask',
    json={'question': user_message}
)

answer = response.json()['answer']
bot.reply(answer)  # Готовый ответ!
```

Полные примеры:
- Telegram Bot - см. `SERVICE_README.md`
- Discord Bot - см. `SERVICE_README.md`
- Python client - см. `example_bot.py`

## 🎓 Что умеют ассистенты

### Code Assistant
- ✅ RAG поиск в документации проекта
- ✅ Поиск по коду Kotlin (классы, функции)
- ✅ Git контекст (текущая ветка, изменения)
- ✅ Интерактивный режим с просмотром файлов

### Support Assistant
- ✅ RAG поиск в FAQ и документации
- ✅ Контекст пользователя из CRM (подписка, устройство)
- ✅ Поиск похожих тикетов
- ✅ Персонализированные ответы
- ✅ REST API для ботов

## 🔧 Дополнительные инструменты

### MCP серверы

```bash
# Git MCP сервер
python3 mcp_git_server.py test

# CRM MCP сервер
python3 mcp_crm_server.py test
```

### Code Reviewer

```bash
python3 code_reviewer.py
```

## 📝 Конфигурация

### Данные CRM (Support Assistant)

Редактируйте `crm_data.json`:
- `users[]` - пользователи
- `tickets[]` - тикеты поддержки

### FAQ (Support Assistant)

Редактируйте `project/docs/SUPPORT_FAQ.md` и переиндексируйте:
```bash
python3 support_assistant.py index
```

### Документация проекта (Code Assistant)

Добавьте `.md` файлы в `project/docs/` и переиндексируйте:
```bash
python3 code_assistant.py index
```

## ✅ Проверка работы

```bash
# Code Assistant
python3 code_assistant.py "ApiService"

# Support Assistant
python3 support_assistant.py ask "Как восстановить пароль?"

# Support Service (требует установки Flask)
source venv/bin/activate
python3 support_service.py
# В другом терминале:
curl http://localhost:5000/health
```

## 🎯 Начните отсюда

1. **Быстрый старт**: Читайте `QUICK_START.md`
2. **Подробное руководство**: Читайте `HOW_TO_USE.md`
3. **REST API для ботов**: Читайте `SERVICE_README.md`

---

**Нужна помощь?** Откройте `HOW_TO_USE.md` или `QUICK_START.md`
