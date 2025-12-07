# 📋 Шпаргалка по командам

## 💻 Code Assistant - Вопросы о коде

```bash
# Интерактивный режим
python3 assistant/code_assistant.py

# Один вопрос
python3 assistant/code_assistant.py "Как использовать ApiService?"

# Индексация документации
python3 assistant/code_assistant.py index

# Справка
python3 assistant/code_assistant.py help
```

## 🎫 Support Assistant - Вопросы поддержки

```bash
# Интерактивный режим
python3 assistant/support_assistant.py

# Вопрос с email
python3 assistant/support_assistant.py ask "Почему не работает авторизация?" user@email.com

# Вопрос без email
python3 assistant/support_assistant.py ask "Как восстановить пароль?"

# Индексация документации
python3 assistant/support_assistant.py index

# Тестовый режим
python3 assistant/support_assistant.py test
```

## 🎯 Когда что использовать?

| Вопрос о... | Используйте |
|-------------|-------------|
| Коде проекта, классах, методах | `code_assistant.py` |
| Пользователях, тикетах, поддержке | `support_assistant.py` |

