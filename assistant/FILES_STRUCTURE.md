# Структура файлов Assistant

## 📂 Основные Python файлы (7)

| Файл | Назначение | Использование |
|------|-----------|---------------|
| `code_assistant.py` | Code Assistant - вопросы о коде | `python3 code_assistant.py "вопрос"` |
| `support_assistant.py` | Support Assistant - техподдержка | `python3 support_assistant.py ask "вопрос"` |
| `support_service.py` | REST API для Support Assistant | `python3 support_service.py` |
| `simple_rag.py` | RAG система (используется обоими) | Библиотека |
| `mcp_git_server.py` | MCP сервер для git | `python3 mcp_git_server.py` |
| `mcp_crm_server.py` | MCP сервер для CRM | `python3 mcp_crm_server.py` |
| `code_reviewer.py` | Code reviewer | `python3 code_reviewer.py` |

## 🧪 Вспомогательные Python файлы (2)

| Файл | Назначение |
|------|-----------|
| `example_bot.py` | Пример интеграции бота |
| `test_service.py` | Тестовый клиент REST API |

## 📚 Документация (8 файлов)

### Для пользователей
| Файл | Содержание |
|------|-----------|
| **README.md** | Главная страница, обзор всех ассистентов |
| **QUICK_START.md** | Быстрый старт (начните отсюда!) |
| **HOW_TO_USE.md** | Подробное руководство по использованию |
| **COMMANDS.md** | Справка по всем командам |

### Для Code Assistant
| Файл | Содержание |
|------|-----------|
| **CODE_ASSISTANT_README.md** | Документация Code Assistant |

### Для Support Service (REST API)
| Файл | Содержание |
|------|-----------|
| **SERVICE_README.md** | Документация REST API, примеры интеграции |
| **SERVICE_SUMMARY.md** | Архитектура и deployment |
| **INSTALL.md** | Установка Flask и зависимостей |
| **QUICKREF.md** | Быстрая справка по командам |

## 🗂️ Данные

| Файл | Содержание |
|------|-----------|
| `crm_data.json` | CRM данные (пользователи, тикеты) |
| `rag_index.json` | RAG индекс документации (генерируется) |

## 🛠️ Скрипты

| Файл | Назначение |
|------|-----------|
| `setup_service.sh` | Автоматическая установка Support Service (venv + Flask) |
| `start_service.sh` | Запуск Support Service с проверками |
| `demo_support_assistant.sh` | Демонстрация Support Assistant |

## 📊 Зависимости между файлами

```
code_assistant.py
    ↓
    → simple_rag.py

support_assistant.py
    ↓
    → simple_rag.py

support_service.py
    ↓
    → support_assistant.py
        ↓
        → simple_rag.py

example_bot.py
    ↓
    → support_assistant.py
        ↓
        → simple_rag.py

test_service.py
    ↓
    → HTTP запросы к support_service.py
```

## ✅ Что было удалено

### Python файлы (устаревшие):
- ❌ `assistant.py` → заменен на `code_assistant.py` и `support_assistant.py`
- ❌ `help.py` → заменен полноценными ассистентами
- ❌ `movike_help.py` → заменен полноценными ассистентами
- ❌ `rag_system.py` → дублировал `simple_rag.py`
- ❌ `test_rag.py` → тестовый файл, не нужен
- ❌ `index_classes.py` → встроен в `code_assistant.py`

### Markdown файлы (устаревшие):
- ❌ Старый `README.md` → заменен новым
- ❌ `CODE_REVIEW_README.md` → не относится к ассистентам
- ❌ `review_output.md` → временный файл
- ❌ `REFACTORING_SUMMARY.md` → временный отчет
- ❌ `FORMATTING_FIX.md` → временный fix
- ❌ `SUPPORT_ASSISTANT_README.md` → дублировал `SERVICE_README.md`
- ❌ `SUPPORT_ASSISTANT_SUMMARY.md` → дублировал `SERVICE_SUMMARY.md`

## 🎯 Рекомендуемый порядок чтения документации

1. **README.md** - начните здесь, обзор всех инструментов
2. **QUICK_START.md** - быстрый старт для начинающих
3. **HOW_TO_USE.md** - подробное руководство
4. **CODE_ASSISTANT_README.md** - для работы с Code Assistant
5. **SERVICE_README.md** - для интеграции с ботами через REST API
6. **INSTALL.md** - если нужно установить Flask для REST API

## 📝 Итого файлов

- **Python**: 9 файлов (7 основных + 2 вспомогательных)
- **Markdown**: 8 файлов документации
- **Данные**: 2 файла (crm_data.json, rag_index.json)
- **Скрипты**: 3 shell скрипта

**Всего: 22 файла** (вместо 30+ до очистки)

Все чисто, структурировано и работает! ✅
