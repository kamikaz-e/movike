# 📖 Как использовать ассистенты в консоли

У вас есть два ассистента для разных задач:

1. **Code Assistant** - отвечает на вопросы о **коде проекта**
2. **Support Assistant** - отвечает на вопросы о **поддержке пользователей**

---

## 💻 Code Assistant - Вопросы о коде

### Интерактивный режим
```bash
python3 assistant/code_assistant.py
```

### Один вопрос
```bash
python3 assistant/code_assistant.py "Как использовать ApiService?"
python3 assistant/code_assistant.py "Где находится FeedViewModel?"
python3 assistant/code_assistant.py "Как работает авторизация?"
```

### Индексация документации
```bash
python3 assistant/code_assistant.py index
```

### Справка
```bash
python3 assistant/code_assistant.py help
```

---

## 🎫 Support Assistant - Вопросы поддержки

### Интерактивный режим
```bash
python3 assistant/support_assistant.py
```

### Один вопрос (с email пользователя)
```bash
python3 assistant/support_assistant.py ask "Почему не работает авторизация?" user@example.com
python3 assistant/support_assistant.py ask "Не прошел платеж за подписку"
```

### Индексация документации
```bash
python3 assistant/support_assistant.py index
```

### Тестовый режим
```bash
python3 assistant/support_assistant.py test
```

---

## 📋 Примеры использования

### Пример 1: Вопрос о коде
```bash
$ python3 assistant/code_assistant.py "ApiService"

💻 MOVIKE CODE ASSISTANT
============================================================
❓ Вопрос: ApiService
------------------------------------------------------------
💻 НАЙДЕННЫЕ ФАЙЛЫ КОДА (7):
📁 app/src/main/java/dev/kamikaze/movike/api/ApiService.kt
   Строка 10: interface ApiService {
...
```

### Пример 2: Вопрос поддержки
```bash
$ python3 assistant/support_assistant.py ask "Почему не работает авторизация?" ivan.petrov@example.com

🎬 MOVIKE SUPPORT ASSISTANT
============================================================
Вопрос: Почему не работает авторизация?
Пользователь: ivan.petrov@example.com
------------------------------------------------------------
📚 ИЗ ДОКУМЕНТАЦИИ:
...

👤 ВАШИ ДАННЫЕ:
   Имя: Иван Петров
   Подписка: premium
...

🎫 ПОХОЖИЕ ОБРАЩЕНИЯ (найдено: 1):
• TICK-001: Не работает авторизация
...
```

### Пример 3: Интерактивный режим Code Assistant
```bash
$ python3 assistant/code_assistant.py

💻 MOVIKE CODE ASSISTANT
============================================================

❓ Вопрос: FeedViewModel
🔍 Ищу информацию...

============================================================
📚 ИЗ ДОКУМЕНТАЦИИ:
...

❓ Вопрос: file:app/src/main/java/dev/kamikaze/movike/presentation/ui/viewmodel/FeedViewModel.kt

📄 app/src/main/java/dev/kamikaze/movike/presentation/ui/viewmodel/FeedViewModel.kt:
------------------------------------------------------------
   1 | package dev.kamikaze.movike.presentation.ui.viewmodel
...

❓ Вопрос: exit
👋 До свидания! Удачного кодинга!
```

### Пример 4: Интерактивный режим Support Assistant
```bash
$ python3 assistant/support_assistant.py

🎬 MOVIKE SUPPORT ASSISTANT
============================================================
Добро пожаловать! Я помогу вам с вопросами о приложении Movike.

Вы: user:ivan.petrov@example.com
✓ Пользователь установлен: Иван Петров (ivan.petrov@example.com)
  Активных тикетов: 2

Вы: Почему не работает авторизация?
🤔 Обрабатываю ваш вопрос...
============================================================
...
```

---

## 🔍 Когда какой ассистент использовать?

### Используйте **Code Assistant** когда:
- ✅ Нужно найти класс, метод, функцию в коде
- ✅ Понять как работает часть кода
- ✅ Найти где используется определенный компонент
- ✅ Посмотреть содержимое файла

**Примеры вопросов:**
- "Как использовать ApiService?"
- "Где находится FeedViewModel?"
- "Как работает авторизация в коде?"

### Используйте **Support Assistant** когда:
- ✅ Нужно ответить на вопрос пользователя
- ✅ Посмотреть историю тикетов
- ✅ Найти похожие проблемы
- ✅ Получить контекст пользователя

**Примеры вопросов:**
- "Почему не работает авторизация?" (с контекстом пользователя)
- "Не прошел платеж за подписку"
- "Приложение вылетает при поиске"

---

## 🚀 Быстрый старт

### Первый запуск - индексация документации

```bash
# Индексируем документацию для Code Assistant
python3 assistant/code_assistant.py index

# Индексируем документацию для Support Assistant
python3 assistant/support_assistant.py index
```

### Ежедневное использование

```bash
# Для вопросов о коде
python3 assistant/code_assistant.py "ваш вопрос о коде"

# Для вопросов поддержки
python3 assistant/support_assistant.py ask "вопрос пользователя" email@example.com
```

---

## 💡 Полезные команды

### Code Assistant - интерактивные команды:
- `index` - переиндексировать документацию
- `file:<путь>` - показать содержимое файла
- `code` - включить/выключить поиск в коде
- `exit` - выход

### Support Assistant - интерактивные команды:
- `user:<email>` - указать email пользователя
- `ticket:<id>` - посмотреть детали тикета
- `exit` - выход

---

## 📝 Сравнительная таблица

| Функция | Code Assistant | Support Assistant |
|---------|---------------|-------------------|
| **Назначение** | Вопросы о коде | Вопросы поддержки |
| **RAG документация** | ✅ | ✅ |
| **Поиск в коде** | ✅ | ❌ |
| **CRM данные** | ❌ | ✅ |
| **Тикеты** | ❌ | ✅ |
| **Git контекст** | ✅ | ❌ |
| **Просмотр файлов** | ✅ | ❌ |
| **Интерактивный режим** | ✅ | ✅ |
| **CLI режим** | ✅ | ✅ |

---

## 🔗 Связанные файлы

- `assistant/code_assistant.py` - Code Assistant
- `assistant/support_assistant.py` - Support Assistant  
- `assistant/CODE_ASSISTANT_README.md` - Подробная документация Code Assistant
- `assistant/SUPPORT_ASSISTANT_README.md` - Подробная документация Support Assistant (если есть)

