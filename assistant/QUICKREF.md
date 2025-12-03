# Support Service - Quick Reference

## ⚡ Быстрый старт (30 секунд)

```bash
cd assistant
./setup_service.sh
```

## 🎯 Основные команды

### Установка (один раз)
```bash
python3 -m venv venv
source venv/bin/activate
pip install Flask flask-cors
python support_assistant.py index
```

### Запуск сервиса
```bash
source venv/bin/activate
python support_service.py
```

### Тестирование
```bash
# В другом терминале
source venv/bin/activate
python test_service.py test

# Или просто демо (без Flask)
python3 example_bot.py
```

## 📡 API Endpoints (сервис должен быть запущен)

### Задать вопрос (главный endpoint)
```bash
curl -X POST http://localhost:5000/api/support/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Как восстановить пароль?"}'
```

### С контекстом пользователя
```bash
curl -X POST http://localhost:5000/api/support/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Почему не работает авторизация?", "email": "ivan.petrov@example.com"}'
```

### Health check
```bash
curl http://localhost:5000/health
```

### Статистика
```bash
curl http://localhost:5000/api/stats
```

## 🤖 Интеграция с ботом

```python
import requests

response = requests.post(
    'http://localhost:5000/api/support/ask',
    json={'question': user_message}
)

answer = response.json()['answer']
bot.reply(answer)  # Готово!
```

## 📁 Ключевые файлы

| Файл | Описание |
|------|----------|
| `support_service.py` | REST API сервис |
| `support_assistant.py` | Core ассистент (работает без Flask) |
| `example_bot.py` | Демо интеграции с ботом |
| `setup_service.sh` | Автоматическая установка |
| `SERVICE_README.md` | Полная документация API |
| `INSTALL.md` | Подробная инструкция установки |

## 🔧 Режимы работы

### 1. REST API (для ботов)
```bash
python support_service.py
# http://localhost:5000/api/support/ask
```

### 2. Консольный (без установки)
```bash
python3 support_assistant.py
# Интерактивный режим
```

### 3. CLI (одиночный запрос)
```bash
python3 support_assistant.py ask "вопрос" [email]
```

## 💾 Данные

- **Пользователи**: `crm_data.json` → users[]
- **Тикеты**: `crm_data.json` → tickets[]
- **FAQ**: `project/docs/SUPPORT_FAQ.md`
- **Индекс**: `rag_index.json` (44 чанка)

## ⚙️ Параметры запуска

```bash
python support_service.py --host 0.0.0.0 --port 8080 --debug
```

## 🎓 Примеры вопросов

- "Почему не работает авторизация?"
- "Как восстановить пароль?"
- "Не прошел платеж"
- "Как отменить подписку?"
- "Приложение вылетает"

## 📚 Документация

| Документ | Содержание |
|----------|-----------|
| `INSTALL.md` | Установка и настройка |
| `SERVICE_README.md` | API документация и примеры |
| `SERVICE_SUMMARY.md` | Архитектура и deployment |
| `QUICK_START.md` | Быстрое начало работы |
| `QUICKREF.md` | Этот файл |

## 🚨 Частые проблемы

**"No module named 'flask'"**
```bash
source venv/bin/activate
```

**"externally-managed-environment"**
```bash
# Используйте venv
python3 -m venv venv
source venv/bin/activate
pip install Flask flask-cors
```

**"Connection refused"**
```bash
# Сервис не запущен
python support_service.py
```

## ✅ Проверка работы

```bash
# 1. Запустите сервис
source venv/bin/activate && python support_service.py

# 2. В другом терминале
curl http://localhost:5000/health
# Должно вернуть: {"status": "ok", ...}
```

## 🎯 Что дальше?

1. **Запустите демо**: `python3 example_bot.py`
2. **Установите сервис**: `./setup_service.sh`
3. **Интегрируйте с ботом**: см. `SERVICE_README.md`
4. **Deploy в production**: см. `SERVICE_SUMMARY.md`

---

**Нужна помощь?** Читайте `INSTALL.md` или `SERVICE_README.md`
