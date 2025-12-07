# 🚀 Быстрый старт - Ассистенты Movike

## Два ассистента - две задачи:

### 1️⃣ Code Assistant - Вопросы о коде
```bash
python3 assistant/code_assistant.py "Как использовать ApiService?"
```

### 2️⃣ Support Assistant - Вопросы поддержки
```bash
python3 assistant/support_assistant.py ask "Почему не работает авторизация?" user@email.com
```

---

## 💻 Code Assistant - Быстрые команды

```bash
# Интерактивный режим
python3 assistant/code_assistant.py

# Один вопрос
python3 assistant/code_assistant.py "ваш вопрос"

# Индексация документации
python3 assistant/code_assistant.py index
```

**Что умеет:**
- ✅ Ищет в документации (RAG)
- ✅ Ищет в коде проекта (.kt файлы)
- ✅ Показывает git контекст
- ✅ Позволяет просматривать файлы

---

## 🎫 Support Assistant - Быстрые команды

```bash
# Интерактивный режим
python3 assistant/support_assistant.py

# Вопрос с email пользователя
python3 assistant/support_assistant.py ask "вопрос" user@email.com

# Вопрос без email
python3 assistant/support_assistant.py ask "вопрос"
```

**Что умеет:**
- ✅ Ищет в документации (RAG)
- ✅ Использует данные CRM (пользователи, тикеты)
- ✅ Находит похожие обращения
- ✅ Персонализирует ответы

---

## 📝 Первый запуск

Выполните индексацию документации для обоих ассистентов:

```bash
python3 assistant/code_assistant.py index
python3 assistant/support_assistant.py index
```

---

## 🎯 Примеры

### Вопрос о коде:
```bash
python3 assistant/code_assistant.py "Где находится FeedViewModel?"
python3 assistant/code_assistant.py "ApiService"
python3 assistant/code_assistant.py "Как работает авторизация?"
```

### Вопрос поддержки:
```bash
python3 assistant/support_assistant.py ask "Почему не работает авторизация?" ivan.petrov@example.com
python3 assistant/support_assistant.py ask "Не прошел платеж"
```

---

## 📚 Подробная документация

- `HOW_TO_USE.md` - Подробная инструкция по использованию
- `CODE_ASSISTANT_README.md` - Документация Code Assistant
- `SUPPORT_ASSISTANT_README.md` - Документация Support Assistant (если есть)
