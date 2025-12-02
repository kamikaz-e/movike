# Movike Project Assistant

AI-ассистент для работы с проектом Movike через RAG и MCP.

## 📁 Структура

```
assistant/
├── README.md                  # Эта документация
├── assistant.py              # Главный скрипт (единая точка входа)
├── simple_rag.py             # RAG система
├── rag_system.py             # RAG с SQLite (альтернативная)
├── index_classes.py          # Индексация классов Kotlin
├── mcp_git_server.py         # MCP сервер для git
├── rag_index.json            # RAG индекс (генерируется)
├── classes_index.json        # Индекс классов (генерируется)
└── rag_database.db           # SQLite база (опционально)
```

## 🚀 Быстрый старт

### Из Claude Code (команда /help)

Просто используй команду `/help`:

```
/help Как использовать ApiService?
/help Какая структура проекта?
/help Расскажи о текущей ветке
```

### Из терминала / logcat консоли

```bash
# Перейди в папку docs
cd project/docs

# Задай вопрос
python3 assistant/assistant.py help "Как использовать ApiService?"

# Или запусти интерактивный режим
python3 assistant/assistant.py
```

## 📖 Команды

### 1. `help` - Задать вопрос о проекте

Самая важная команда. Ищет ответ в RAG базе и возвращает результаты.

```bash
python3 assistant/assistant.py help "ваш вопрос"
```

**Примеры:**
```bash
python3 assistant/assistant.py help "ApiService"
python3 assistant/assistant.py help "структура проекта"
python3 assistant/assistant.py help "FeedViewModel"
python3 assistant/assistant.py help "как использовать Logger"
```

**Вывод:**
```
============================================================
  Movike Assistant - Вопрос: ApiService
============================================================

🔍 Поиск в RAG базе данных...

✅ Найдено результатов: 3

------------------------------------------------------------

📄 Результат #1
   Файл: app/src/main/java/dev/kamikaze/movike/api/ApiService.kt:10
   Релевантность: 1

   Содержимое:
   --------------------------------------------------------
   # interface ApiService

   **Файл:** app/src/main/java/dev/kamikaze/movike/api/ApiService.kt:10

   **Код:**
   ```kotlin
   interface ApiService {

       @GET("discover/movie")
       suspend fun apiMainMovie(
           @Query("page") page: Int
       ): MovieListResponse

       @GET("search/movie")
       suspend fun apiSearchMovie(
           @Query("query") query: String,
           @Query("page") page: Int
       ): MovieListResponse

       @GET("movie/{movie_id}")
       suspend fun apiMovie(
           @Path("movie_id") movieId: Int
       ): Response<Movie>
   }
   ```
   --------------------------------------------------------
```

### 2. `search` - Прямой поиск

Поиск ключевых слов в RAG базе (без форматированного вывода).

```bash
python3 assistant/assistant.py search "Repository"
```

### 3. `git` - Информация о git ветке

Получает информацию через MCP сервер.

```bash
python3 assistant/assistant.py git
```

**Вывод:**
```
📊 Git информация через MCP

=== Тест MCP Git Server ===

1. Текущая ветка:
   sketch

2. Информация о ветке:
{
  "current_branch": "sketch",
  "status": "## sketch...origin/sketch",
  "last_commit": "b5a99ed добавил проверку открытых файлов",
  "all_branches": ["sketch"]
}
```

### 4. `stats` - Статистика RAG

Показывает, сколько документов проиндексировано.

```bash
python3 assistant/assistant.py stats
```

**Вывод:**
```
📈 Статистика RAG системы

Всего документов: 150

📚 Документация:
  README.md: 7 чанков
  project/docs/API_REFERENCE.md: 13 чанков
  project/docs/CODE_STYLE.md: 19 чанков
  project/docs/PROJECT_STRUCTURE.md: 7 чанков

💻 Классы проекта: 104 файлов

✅ Всего в RAG: 150 документов
```

### 5. `reindex` - Переиндексация

Полная переиндексация документации и классов.

```bash
python3 assistant/assistant.py reindex
```

**Когда использовать:**
- После изменения документации
- После добавления новых классов
- Если поиск не находит недавно добавленный код

### 6. Интерактивный режим

Запусти без аргументов для интерактивного режима:

```bash
python3 assistant/assistant.py
```

или

```bash
python3 assistant/assistant.py interactive
```

**Пример сессии:**
```
============================================================
  🤖 Movike Project Assistant - Интерактивный режим
============================================================

Команды:
  help <вопрос>  - Задать вопрос о проекте
  search <текст> - Поиск в документации
  git            - Информация о git ветке
  stats          - Статистика RAG
  reindex        - Переиндексация
  exit           - Выход

============================================================

Assistant> help ApiService
[Вывод результатов...]

Assistant> git
[Информация о git...]

Assistant> exit
Выход...
```

## 🎯 Использование из logcat консоли Android Studio

### Вариант 1: Через терминал Android Studio

1. Открой Terminal в Android Studio (Alt+F12 / Cmd+T)
2. Перейди в папку docs:
   ```bash
   cd project/docs
   ```
3. Запусти assistant:
   ```bash
   python3 assistant/assistant.py help "ваш вопрос"
   ```

### Вариант 2: Создай alias

Добавь в `~/.bashrc` или `~/.zshrc`:

```bash
alias movike-help='python3 /Users/admin/StudioProjects/movike/project/docs/assistant/assistant.py help'
alias movike-assist='python3 /Users/admin/StudioProjects/movike/project/docs/assistant/assistant.py'
```

Теперь можно использовать из любого места:

```bash
movike-help "ApiService"
movike-assist git
movike-assist stats
```

### Вариант 3: Через Run Configuration

1. В Android Studio: Run → Edit Configurations
2. Добавь новую Python configuration:
   - Script: `/Users/admin/StudioProjects/movike/project/docs/assistant/assistant.py`
   - Parameters: `help "ApiService"`
3. Запускай через Shift+F10

## 📊 Что покрывает RAG

**Документация (46 чанков):**
- README.md
- project/docs/PROJECT_STRUCTURE.md
- project/docs/API_REFERENCE.md
- project/docs/CODE_STYLE.md

**Классы проекта (104 класса):**
- ApiService, Repository, RepositoryImpl
- ViewModels: FeedViewModel, SearchViewModel, DetailsMovieViewModel
- Fragments: FeedFragment, SearchFragment, DetailsFragment
- Adapters, ViewHolders, UseCases
- Database: AppDatabase, DAOs
- DI modules: ApiModule, DataModule, ViewModelModule
- И многое другое...

**Всего: 150 документов в RAG базе**

## 🔧 Архитектура

```
┌─────────────────────────────────────────┐
│        assistant.py (main entry)        │
│   Единая точка входа для всех команд    │
└─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
        ▼                       ▼
┌──────────────┐       ┌──────────────┐
│  simple_rag  │       │ mcp_git_     │
│     .py      │       │  server.py   │
│              │       │              │
│ • Поиск в    │       │ • Git branch │
│   документах │       │ • Git status │
│ • Индексация │       │ • Открытые   │
│              │       │   файлы      │
└──────────────┘       └──────────────┘
        │
        ▼
┌──────────────┐
│ index_       │
│  classes.py  │
│              │
│ • Сканирует  │
│   Kotlin код │
│ • Извлекает  │
│   классы     │
└──────────────┘
```

## 💡 Советы и трюки

### Эффективные вопросы

**✅ Хорошо:**
- "ApiService" (конкретный класс)
- "FeedViewModel" (конкретный класс)
- "структура проекта модули" (ключевые слова)
- "Repository pattern" (паттерн)

**❌ Плохо:**
- "как это работает?" (слишком расплывчато)
- "покажи код" (нужно указать что именно)

### Поиск классов

Для поиска классов просто укажи имя:
```bash
python3 assistant/assistant.py help "SearchViewModel"
python3 assistant/assistant.py help "MovieAdapter"
```

### Поиск по теме

Для широкого поиска используй ключевые слова:
```bash
python3 assistant/assistant.py help "navigation навигация"
python3 assistant/assistant.py help "database dao"
python3 assistant/assistant.py help "viewmodel lifecycle"
```

## 🐛 Отладка

### Проблема: Не находит недавно добавленный класс

**Решение:**
```bash
python3 assistant/assistant.py reindex
```

### Проблема: Ошибка "No module named 'simple_rag'"

**Решение:** Запускай из папки `project/docs`:
```bash
cd /Users/admin/StudioProjects/movike/project/docs
python3 assistant/assistant.py help "вопрос"
```

### Проблема: RAG индекс не найден

**Решение:**
```bash
# Сначала переиндексируй
python3 assistant/assistant.py reindex

# Потом попробуй снова
python3 assistant/assistant.py help "вопрос"
```

## 📝 Примеры реальных вопросов

### 1. Узнать о классе

```bash
python3 assistant/assistant.py help "ApiService"
```

Вернёт интерфейс ApiService с методами API.

### 2. Узнать структуру проекта

```bash
python3 assistant/assistant.py help "структура проекта"
```

Вернёт информацию о модулях, архитектуре, зависимостях.

### 3. Узнать стиль кода

```bash
python3 assistant/assistant.py help "Composable функции именование"
```

Вернёт правила именования для Composable функций.

### 4. Информация о ViewModel

```bash
python3 assistant/assistant.py help "FeedViewModel"
```

Вернёт код FeedViewModel с зависимостями.

### 5. Текущая git ветка

```bash
python3 assistant/assistant.py git
```

Вернёт информацию о текущей ветке, коммитах, статусе.

## 🎓 Заключение

Movike Project Assistant - это мощный инструмент для работы с проектом:

- ✅ **150 документов** в RAG базе
- ✅ **104 класса** проиндексировано
- ✅ **RAG** для поиска в документации и коде
- ✅ **MCP** для git информации
- ✅ **Работает из любого места** (терминал, logcat, Claude Code)
- ✅ **Интерактивный режим** для удобства

Используй `python3 assistant/assistant.py help "ваш вопрос"` для получения информации о проекте!
