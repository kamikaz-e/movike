# 🤖 AI Code Reviewer для Pull Requests

Автоматическая система ревью кода на основе AI, использующая RAG для контекста и MCP для получения информации о PR.

## 📋 Возможности

Система автоматически анализирует каждый PR и выдает:

- **Найденные проблемы** - потенциальные ошибки в коде
- **Потенциальные баги** - memory leaks, неправильное использование корутин, и т.д.
- **Советы по улучшению** - рекомендации по стилю и best practices
- **Связанная документация** - ссылки на релевантные части документации из RAG

## 🏗️ Архитектура

```
┌─────────────────────────────────────────────────────────────┐
│                      GitHub Pull Request                      │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              GitHub Actions Workflow                         │
│              (.github/workflows/code-review.yml)             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Code Reviewer                              │
│              (assistant/code_reviewer.py)                    │
│                                                               │
│  ┌──────────────┐         ┌────────────────┐                │
│  │  MCP Server  │◄────────│  RAG System    │                │
│  │              │         │                │                │
│  │ - get_pr_diff│         │ - Документация │                │
│  │ - get_files  │         │ - Контекст     │                │
│  │ - get_content│         │ - История      │                │
│  └──────────────┘         └────────────────┘                │
│         │                         │                          │
│         └─────────┬───────────────┘                          │
│                   ▼                                          │
│          ┌─────────────────┐                                │
│          │ Code Analysis   │                                │
│          │ - Kotlin checks │                                │
│          │ - Bug detection │                                │
│          │ - Suggestions   │                                │
│          └─────────────────┘                                │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│               Review Comment on PR                           │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Быстрый старт

### 1. Локальное тестирование

```bash
# Перейти в директорию assistant
cd assistant

# Индексировать документацию
python3 -c "from simple_rag import SimpleRAG; rag = SimpleRAG(); rag.index_all()"

# Запустить ревью для текущей ветки
python3 code_reviewer.py main

# Результат сохранится в review_output.md
cat review_output.md
```

### 2. Настройка для GitHub Actions

Workflow уже настроен в `.github/workflows/code-review.yml` и будет запускаться автоматически при:

- Создании нового PR
- Обновлении существующего PR (новые коммиты)
- Повторном открытии PR

### 3. Проверка работы

1. Создайте тестовую ветку:
```bash
git checkout -b test-code-review
```

2. Внесите изменения в Kotlin файлы

3. Закоммитьте и создайте PR:
```bash
git add .
git commit -m "test: проверка code review"
git push origin test-code-review
```

4. Откройте PR на GitHub - автоматическое ревью появится в комментариях

## 🔍 Что проверяется

### Kotlin Code Checks

#### ⚠️ Проблемы:
- `TODO/FIXME` комментарии в коде
- Использование `println()` в продакшн коде
- Force unwrap `!!` без обработки
- Пустые `catch` блоки

#### 🐛 Потенциальные баги:
- Утечки памяти (неочищенные listeners)
- Использование `GlobalScope` вместо `lifecycleScope`/`viewModelScope`
- Корутины без явного `Dispatcher`
- Хранение `Context` в `ViewModel`

#### 💡 Советы по улучшению:
- Использование `?.let {}` вместо `if != null`
- `when` вместо множественных `if-else`
- `const val` для констант

## 📚 Использование RAG

RAG система используется для:

1. **Контекста проекта** - понимание архитектуры и паттернов
2. **Связанной документации** - ссылки на релевантные секции README и docs
3. **Исторического контекста** - предыдущие решения похожих задач

Документация индексируется из:
- `README.md`
- `project/docs/*.md`
- Kotlin классы проекта (через `index_classes.py`)

## 🔧 Компоненты системы

### 1. MCP Server (`mcp_git_server.py`)

Предоставляет инструменты для работы с git:

- `get_pr_diff(base, head)` - получить diff между ветками
- `get_pr_files(base)` - список измененных файлов
- `get_file_content(path, ref)` - содержимое файла из git

### 2. RAG System (`simple_rag.py`)

Система индексации и поиска документации:

- Индексация markdown файлов
- Полнотекстовый поиск
- Ранжирование результатов по релевантности

### 3. Code Reviewer (`code_reviewer.py`)

Основной анализатор кода:

- Получение PR контекста через MCP
- Анализ каждого измененного файла
- Поиск связанной документации в RAG
- Генерация отчета в Markdown

## 📊 Пример отчета

```markdown
# 🤖 AI Code Review

**Base branch:** `main`
**Head branch:** `feature/new-screen`
**Files changed:** 3

---

## 📄 `app/src/main/java/com/example/MainActivity.kt`

**Status:** M

### ⚠️ Проблемы:

- Line 42: Использование !! (force unwrap) может привести к NPE
- Line 78: Использование println() в продакшн коде

### 🐛 Потенциальные баги:

- Line 95: Убедитесь, что listener очищается в onDestroy/onDestroyView

### 💡 Советы по улучшению:

- Line 56: Рассмотрите использование ?.let { } вместо if != null

### 📚 Связанная документация:

- `README.md` (релевантность: 3)

---

## 📊 Сводка

- **Всего проблем:** 2
- **Потенциальных багов:** 1
- **Предложений по улучшению:** 1

### ⚠️ Рекомендация: Рассмотрите исправление найденных проблем

---
*Автоматическое ревью сгенерировано AI Code Reviewer*
```

## ⚙️ Конфигурация

### GitHub Actions

Workflow конфигурация в `.github/workflows/code-review.yml`:

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened]
    branches:
      - main
      - master
      - develop
      - sketch
```

### Переменные окружения

- `GITHUB_BASE_REF` - базовая ветка (автоматически в GitHub Actions)
- `GITHUB_STEP_SUMMARY` - путь для GitHub Actions summary (автоматически)

### Аргументы командной строки

```bash
python3 code_reviewer.py [base_branch]

# Примеры:
python3 code_reviewer.py main
python3 code_reviewer.py develop
python3 code_reviewer.py sketch
```

## 🔒 Требования

### Минимальные:
- Python 3.8+
- Git
- Доступ к репозиторию

### Зависимости:
Нет внешних зависимостей! Используются только встроенные модули Python.

### Для GitHub Actions:
- Разрешения: `contents: read`, `pull-requests: write`

## 🎯 Расширение функционала

### Добавление новых проверок

Отредактируйте методы в `code_reviewer.py`:

```python
def _check_kotlin_issues(self, content: str, file_path: str) -> List[str]:
    """Добавьте свои проверки здесь"""
    issues = []

    # Ваша проверка
    if 'my_pattern' in content:
        issues.append("Найден паттерн my_pattern")

    return issues
```

### Добавление поддержки других языков

```python
# В методе analyze_file_changes()
if file_path.endswith('.java'):
    analysis['issues'].extend(self._check_java_issues(content, file_path))
elif file_path.endswith('.xml'):
    analysis['issues'].extend(self._check_xml_issues(content, file_path))
```

### Интеграция с AI моделями

Для более умного анализа можно интегрировать Claude или другие LLM:

```python
# Добавить в requirements.txt
# anthropic>=0.18.0

import anthropic

def analyze_with_ai(self, code: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": f"Review this code:\n\n{code}"
        }]
    )
    return message.content
```

## 🐛 Отладка

### Просмотр логов GitHub Actions

1. Перейдите в раздел "Actions" вашего репозитория
2. Выберите workflow "AI Code Review"
3. Откройте конкретный запуск
4. Изучите логи каждого шага

### Локальная отладка

```bash
# Включить verbose режим
export DEBUG=1
python3 code_reviewer.py main

# Проверить MCP сервер
python3 mcp_git_server.py test

# Проверить RAG индекс
python3 -c "from simple_rag import SimpleRAG; rag = SimpleRAG(); rag.load_index(); print(len(rag.documents))"
```

## 📝 TODO / Roadmap

- [ ] Интеграция с Claude API для более умного анализа
- [ ] Поддержка Java/XML файлов
- [ ] Анализ gradle.build файлов
- [ ] Проверка архитектурных паттернов (MVVM, Clean Architecture)
- [ ] Детекция дублированного кода
- [ ] Анализ покрытия тестами
- [ ] Проверка безопасности (security vulnerabilities)
- [ ] Интеграция с SonarQube/detekt

## 🤝 Contributing

Предложения и улучшения приветствуются!

1. Форкните репозиторий
2. Создайте feature ветку
3. Сделайте изменения
4. Создайте PR
5. Автоматическое ревью проверит ваш код!

## 📄 Лицензия

Проект использует лицензию проекта Movike.

---

**Создано с помощью:**
- RAG для контекста
- MCP для интеграции с git
- Python встроенных модулей
- GitHub Actions

*AI Code Reviewer - автоматизируйте код ревью и улучшайте качество кода!*
