# ✅ Проверка архитектуры: RAG + MCP в Code Review

Этот документ подтверждает, что система использует **RAG для контекста документации** и **MCP для получения PR данных**.

---

## 📋 Оглавление

1. [Использование RAG для документации](#1-использование-rag-для-документации)
2. [Использование MCP для PR данных](#2-использование-mcp-для-pr-данных)
3. [Поток данных](#3-поток-данных)
4. [Конкретные примеры в коде](#4-конкретные-примеры-в-коде)

---

## 1️⃣ Использование RAG для документации

### ✅ Где используется RAG:

#### **Файл:** `assistant/code_reviewer.py`

### **Инициализация RAG:**

```python
# Строки 18-19: Импорт RAG системы
from simple_rag import SimpleRAG

# Строки 28-33: Создание и загрузка RAG индекса
class CodeReviewer:
    def __init__(self, base_branch: str = "main"):
        self.base_branch = base_branch
        self.project_root = ASSISTANT_DIR.parent
        self.rag = SimpleRAG()  # ← Инициализация RAG
        self.git_server = GitMCPServer()

        # Загружаем RAG индекс
        if self.rag.index_path.exists():
            self.rag.load_index()  # ← Загрузка документации
```

**Что происходит:**
- RAG индекс загружается при создании reviewer
- Индекс содержит документацию из README.md и project/docs/

---

### **Поиск связанной документации:**

```python
# Строки 156-167: Метод для поиска документации
def search_related_docs(self, file_path: str) -> List[Dict[str, Any]]:
    """Ищет связанную документацию в RAG"""
    if not self.rag.documents:
        return []

    # Извлекаем ключевые слова из пути
    keywords = file_path.replace('/', ' ').replace('.kt', '').replace('_', ' ')

    # Ищем в RAG ← ЗДЕСЬ ПРОИСХОДИТ ПОИСК В ДОКУМЕНТАЦИИ
    results = self.rag.search(keywords, limit=3)

    return results
```

**Что происходит:**
- Извлекаются ключевые слова из имени файла
- RAG ищет релевантную документацию
- Возвращаются топ-3 результата

---

### **Добавление документации в отчет:**

```python
# Строки 223-229: Добавление связанной документации в ревью
# Добавляем связанную документацию
docs = self.search_related_docs(file_path)  # ← Поиск через RAG
if docs:
    review.append("### 📚 Связанная документация:\n")
    for doc in docs[:2]:
        review.append(f"- `{doc['file']}` (релевантность: {doc['score']})")
    review.append("")
```

**Что происходит:**
- Для каждого измененного файла ищется связанная документация
- Документация добавляется в отчет с оценкой релевантности

---

### **Индексация документации в GitHub Actions:**

#### **Файл:** `.github/workflows/code-review.yml`

```yaml
# Строки 44-48: Индексация документации перед анализом
- name: Index documentation with RAG
  run: |
    cd assistant
    python3 -c "from simple_rag import SimpleRAG; rag = SimpleRAG(); rag.index_all()"
    echo "✅ RAG indexing completed"
```

**Что происходит:**
- Перед каждым ревью документация переиндексируется
- RAG создает базу знаний из README и docs/

---

## 2️⃣ Использование MCP для PR данных

### ✅ Где используется MCP:

#### **Файл:** `assistant/code_reviewer.py`

### **Инициализация MCP сервера:**

```python
# Строки 19: Импорт MCP сервера
from mcp_git_server import GitMCPServer

# Строка 29: Создание MCP сервера
class CodeReviewer:
    def __init__(self, base_branch: str = "main"):
        self.base_branch = base_branch
        self.project_root = ASSISTANT_DIR.parent
        self.rag = SimpleRAG()
        self.git_server = GitMCPServer()  # ← Инициализация MCP
```

---

### **Получение контекста PR через MCP:**

```python
# Строки 35-50: Получение данных о PR через MCP
def get_pr_context(self) -> Dict[str, Any]:
    """Получает контекст PR через MCP"""
    print("📊 Получение информации о PR...\n")

    # Получаем список измененных файлов ← MCP
    files_info = self.git_server.get_pr_files(self.base_branch)

    # Получаем diff ← MCP
    diff_info = self.git_server.get_pr_diff(self.base_branch)

    return {
        'files': files_info.get('files', []),
        'diff': diff_info.get('diff', ''),
        'base': self.base_branch,
        'head': diff_info.get('head', 'HEAD')
    }
```

**Что происходит:**
- `get_pr_files()` - получает список измененных файлов через MCP
- `get_pr_diff()` - получает полный diff через MCP
- Возвращается контекст PR для анализа

---

### **Получение содержимого файлов через MCP:**

```python
# Строки 52-62: Анализ конкретного файла
def analyze_file_changes(self, file_path: str, status: str) -> Dict[str, Any]:
    analysis = {
        'file': file_path,
        'status': status,
        'issues': [],
        'suggestions': [],
        'potential_bugs': []
    }

    # Получаем содержимое файла ← MCP
    file_content = self.git_server.get_file_content(file_path)
```

**Что происходит:**
- MCP получает содержимое файла из git
- Файл анализируется на проблемы

---

### **MCP методы в git_server.py:**

#### **Файл:** `assistant/mcp_git_server.py`

### **1. Получение diff:**

```python
# Строки 277-297: Метод для получения diff
def get_pr_diff(self, base: str = "main", head: str = None) -> Dict[str, Any]:
    """Получает diff между ветками"""
    try:
        if head is None:
            head = self.get_current_branch()

        result = subprocess.run(
            ['git', 'diff', f'{base}...{head}'],  # ← GIT DIFF
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            'base': base,
            'head': head,
            'diff': result.stdout,
            'success': result.returncode == 0
        }
    except Exception as e:
        return {'error': str(e), 'success': False}
```

**Что происходит:**
- Выполняется `git diff base...head`
- Возвращается полный diff изменений

---

### **2. Получение списка файлов:**

```python
# Строки 299-327: Метод для получения списка файлов
def get_pr_files(self, base: str = "main") -> Dict[str, Any]:
    """Получает список измененных файлов"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-status', f'{base}...HEAD'],  # ← GIT DIFF
            capture_output=True,
            text=True,
            timeout=10
        )

        files = []
        for line in result.stdout.strip().split('\n'):
            if line:
                parts = line.split('\t')
                if len(parts) == 2:
                    status, filepath = parts
                    files.append({
                        'status': status,  # A=Added, M=Modified, D=Deleted
                        'path': filepath
                    })

        return {
            'base': base,
            'files': files,
            'count': len(files),
            'success': result.returncode == 0
        }
    except Exception as e:
        return {'error': str(e), 'success': False}
```

**Что происходит:**
- Выполняется `git diff --name-status`
- Возвращается список файлов со статусом (A/M/D)

---

### **3. Получение содержимого файла:**

```python
# Строки 329-346: Метод для получения содержимого
def get_file_content(self, file_path: str, ref: str = "HEAD") -> Dict[str, Any]:
    """Получает содержимое файла из git"""
    try:
        result = subprocess.run(
            ['git', 'show', f'{ref}:{file_path}'],  # ← GIT SHOW
            capture_output=True,
            text=True,
            timeout=10
        )

        return {
            'file_path': file_path,
            'ref': ref,
            'content': result.stdout,
            'success': result.returncode == 0
        }
    except Exception as e:
        return {'error': str(e), 'success': False}
```

**Что происходит:**
- Выполняется `git show ref:file_path`
- Возвращается полное содержимое файла

---

## 3️⃣ Поток данных

### Полный цикл анализа PR:

```
┌─────────────────────────────────────────────────────────────┐
│                    GitHub Pull Request                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│           GitHub Actions Workflow запускается                │
│           (.github/workflows/code-review.yml)                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 1: Index documentation with RAG                        │
│  → python3 -c "...SimpleRAG().index_all()"                   │
│  → Индексирует README.md + project/docs/*.md                │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│  Step 2: Run AI Code Review                                  │
│  → python3 code_reviewer.py sketch                           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              CodeReviewer.__init__()                         │
│  ┌────────────────────┐   ┌────────────────────┐           │
│  │  RAG System        │   │  MCP Server        │           │
│  │  - Load index      │   │  - Initialize git  │           │
│  │  - Load docs       │   │  - Prepare tools   │           │
│  └────────────────────┘   └────────────────────┘           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│            get_pr_context() через MCP                        │
│  ┌──────────────────────────────────────────────┐           │
│  │ MCP: get_pr_files(base)                      │           │
│  │ → git diff --name-status sketch...HEAD       │           │
│  │ → Возвращает: [file1.kt, file2.kt, ...]     │           │
│  └──────────────────────────────────────────────┘           │
│  ┌──────────────────────────────────────────────┐           │
│  │ MCP: get_pr_diff(base)                       │           │
│  │ → git diff sketch...HEAD                     │           │
│  │ → Возвращает: полный diff                   │           │
│  └──────────────────────────────────────────────┘           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│        Для каждого файла: analyze_file_changes()             │
│  ┌──────────────────────────────────────────────┐           │
│  │ MCP: get_file_content(file_path)             │           │
│  │ → git show HEAD:file_path                    │           │
│  │ → Возвращает: содержимое файла              │           │
│  └──────────────────────────────────────────────┘           │
│  ┌──────────────────────────────────────────────┐           │
│  │ Анализ кода:                                 │           │
│  │ → _check_kotlin_issues()                     │           │
│  │ → _check_kotlin_bugs()                       │           │
│  │ → _check_kotlin_suggestions()                │           │
│  └──────────────────────────────────────────────┘           │
│  ┌──────────────────────────────────────────────┐           │
│  │ RAG: search_related_docs(file_path)          │           │
│  │ → rag.search(keywords)                       │           │
│  │ → Возвращает: связанную документацию        │           │
│  └──────────────────────────────────────────────┘           │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              generate_review()                               │
│  Объединяет:                                                 │
│  - Проблемы из анализа                                       │
│  - Документацию из RAG                                       │
│  - Контекст из MCP                                           │
│  → Создает review_output.md                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│          Post review as comment (GitHub Actions)             │
│  → Комментарий в PR с полным отчетом                         │
└─────────────────────────────────────────────────────────────┘
```

---

## 4️⃣ Конкретные примеры в коде

### Пример 1: RAG ищет документацию

**Входные данные:**
- Измененный файл: `app/src/main/java/com/example/MainActivity.kt`

**Процесс:**
```python
# code_reviewer.py:224
docs = self.search_related_docs(file_path)
# ↓
# code_reviewer.py:162
keywords = "app src main java com example MainActivity"
# ↓
# simple_rag.py:search()
results = rag.search("app src main java com example MainActivity", limit=3)
```

**Результат:**
```markdown
### 📚 Связанная документация:
- `README.md` (релевантность: 3)
- `project/docs/architecture.md` (релевантность: 2)
```

---

### Пример 2: MCP получает список файлов

**Процесс:**
```python
# code_reviewer.py:40
files_info = self.git_server.get_pr_files(self.base_branch)
# ↓
# mcp_git_server.py:299
subprocess.run(['git', 'diff', '--name-status', 'sketch...HEAD'])
```

**Результат:**
```json
{
  "base": "sketch",
  "files": [
    {"status": "M", "path": "app/src/main/MainActivity.kt"},
    {"status": "A", "path": "app/src/main/NewScreen.kt"},
    {"status": "D", "path": "app/src/main/OldFile.kt"}
  ],
  "count": 3
}
```

---

### Пример 3: MCP получает содержимое файла

**Процесс:**
```python
# code_reviewer.py:60
file_content = self.git_server.get_file_content(file_path)
# ↓
# mcp_git_server.py:329
subprocess.run(['git', 'show', 'HEAD:app/src/main/MainActivity.kt'])
```

**Результат:**
```json
{
  "file_path": "app/src/main/MainActivity.kt",
  "ref": "HEAD",
  "content": "package com.example\n\nclass MainActivity {...}",
  "success": true
}
```

---

## ✅ Итоговая проверка

### RAG используется для:

| Функция | Файл | Строки | Что делает |
|---------|------|--------|------------|
| ✅ Инициализация | `code_reviewer.py` | 28-33 | Загружает RAG индекс |
| ✅ Поиск документации | `code_reviewer.py` | 156-167 | Ищет связанные docs |
| ✅ Добавление в отчет | `code_reviewer.py` | 223-229 | Показывает docs в ревью |
| ✅ Индексация | `.github/workflows/code-review.yml` | 44-48 | Переиндексирует перед ревью |

### MCP используется для:

| Функция | Файл | Строки | Что делает |
|---------|------|--------|------------|
| ✅ Инициализация | `code_reviewer.py` | 29 | Создает MCP сервер |
| ✅ Получение файлов | `code_reviewer.py` | 40 | Список измененных файлов |
| ✅ Получение diff | `code_reviewer.py` | 43 | Полный diff PR |
| ✅ Получение содержимого | `code_reviewer.py` | 60 | Содержимое каждого файла |
| ✅ Git diff | `mcp_git_server.py` | 277-297 | Реализация git diff |
| ✅ Git name-status | `mcp_git_server.py` | 299-327 | Реализация списка файлов |
| ✅ Git show | `mcp_git_server.py` | 329-346 | Реализация получения файла |

---

## 🎯 Заключение

**✅ Подтверждаю:**

1. **RAG используется для контекста документации:**
   - Индексирует README.md и project/docs/
   - Ищет связанную документацию для каждого файла
   - Добавляет ссылки в отчет ревью

2. **MCP используется для получения PR данных:**
   - Получает список измененных файлов
   - Получает полный diff изменений
   - Получает содержимое каждого файла

3. **Интеграция работает:**
   - RAG + MCP работают вместе в `code_reviewer.py`
   - GitHub Actions автоматически запускает обе системы
   - Результат объединяется в единый отчет

**Все требования выполнены! 🎉**

---

*Документ создан для проверки архитектуры системы автоматического ревью кода.*
