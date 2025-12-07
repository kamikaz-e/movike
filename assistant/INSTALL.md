# Installation Guide - Support Service

## 🚀 Автоматическая установка (Рекомендуется)

### Вариант 1: Полная автоматическая установка

```bash
cd assistant
./setup_service.sh
```

Скрипт автоматически:
- Создаст виртуальное окружение
- Установит все зависимости (Flask, flask-cors, gunicorn)
- Проиндексирует документацию
- Предложит запустить сервис

### Вариант 2: Ручная установка с виртуальным окружением

```bash
cd assistant

# 1. Создать виртуальное окружение
python3 -m venv venv

# 2. Активировать виртуальное окружение
source venv/bin/activate

# 3. Установить зависимости
pip install Flask flask-cors gunicorn

# 4. Проиндексировать документацию
python support_assistant.py index

# 5. Запустить сервис
python support_service.py
```

## 📦 Зависимости

Все зависимости устанавливаются в изолированное виртуальное окружение:

```
Flask>=3.0.0          # Web framework
flask-cors>=4.0.0     # CORS support
gunicorn>=21.2.0      # Production server (опционально)
```

## 🎯 Проверка установки

После установки проверьте работу:

```bash
# В терминале 1: запуск сервиса
source venv/bin/activate
python support_service.py

# В терминале 2: тест
source venv/bin/activate
python test_service.py test
```

## 🐍 Без Flask (только демонстрация)

Если вы не хотите устанавливать Flask, можете запустить демонстрацию:

```bash
# Демо бота (работает без Flask)
python3 example_bot.py

# Консольный режим
python3 support_assistant.py
```

## 🔧 Troubleshooting

### Проблема: "error: externally-managed-environment"

Это нормально для систем с Homebrew Python. **Решение:**

```bash
# Используйте виртуальное окружение (рекомендуется)
python3 -m venv venv
source venv/bin/activate
pip install Flask flask-cors
```

### Проблема: "No module named 'flask'"

```bash
# Убедитесь, что виртуальное окружение активировано
source venv/bin/activate

# Проверьте установку
python -c "import flask; print(flask.__version__)"
```

### Проблема: "permission denied"

```bash
# Сделайте скрипты исполняемыми
chmod +x setup_service.sh
chmod +x start_service.sh
```

## 🚀 Запуск после установки

### Каждый раз при запуске:

```bash
cd assistant
source venv/bin/activate
python support_service.py
```

### Или через скрипт:

```bash
cd assistant
source venv/bin/activate && python support_service.py
```

## 📝 Структура после установки

```
assistant/
├── venv/                       # Виртуальное окружение (создается)
│   ├── bin/
│   ├── lib/
│   └── ...
├── support_service.py          # REST API сервис
├── support_assistant.py        # Core ассистент
├── simple_rag.py              # RAG система
├── crm_data.json              # Данные CRM
├── rag_index.json             # Индекс документации (создается)
├── setup_service.sh           # Скрипт установки
└── requirements.txt           # Зависимости
```

## ✅ Готово!

После установки сервис будет доступен на:
```
http://localhost:5001
```

**Тестирование:**
```bash
# Health check
curl http://localhost:5001/health

# Задать вопрос
curl -X POST http://localhost:5001/api/support/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Как восстановить пароль?"}'
```

## 🎯 Следующие шаги

1. **Интеграция с ботом** - см. `SERVICE_README.md`
2. **Production deployment** - см. `SERVICE_SUMMARY.md`
3. **API документация** - см. `SERVICE_README.md`

## 💡 Примечания

- **Виртуальное окружение** изолирует зависимости от системного Python
- **Не нужны права sudo** - все устанавливается локально
- **Легко удалить** - просто удалите папку `venv/`
- **Работает на macOS с Homebrew** - обходит ограничения PEP 668
