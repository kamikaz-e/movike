# How to Run Code Review Script

This guide shows you how to run the code review script to check all files with intentional errors.

## Quick Start

### Option 1: Run from Terminal

```bash
cd /Users/admin/StudioProjects/movike
python3 assistant/code_reviewer.py sketch
```

This will:
- Analyze all changed files compared to the `sketch` branch
- Use RAG system for documentation context
- Use MCP for git operations
- Generate a detailed report

### Option 2: Use the Helper Script

```bash
/tmp/check_bad_code.sh
```

### Option 3: Run from Android Studio Terminal

1. Open Terminal in Android Studio (Alt+F12 / Cmd+T)
2. Run:
   ```bash
   python3 assistant/code_reviewer.py sketch
   ```

## What Gets Checked

The code reviewer checks these 5 files with intentional errors:

### 1. **ApiService.kt** - API Design Issues
- ❌ Blocking calls without `suspend` modifier
- ❌ Hardcoded API key: `api_key=12345abcde`
- ❌ Inconsistent error handling

**Location:** `app/src/main/java/dev/kamikaze/movike/api/ApiService.kt`

### 2. **RepositoryImpl.kt** - Memory Leaks
- ❌ GlobalScope usage (coroutine leaks)
- ❌ FileOutputStream not closed (resource leak)
- ❌ `runBlocking` usage (blocking operations)
- ❌ Database operations on main thread

**Location:** `app/src/main/java/dev/kamikaze/movike/repository/RepositoryImpl.kt`

### 3. **FeedViewModel.kt** - ViewModel Bad Practices
- ❌ Public mutable LiveData
- ❌ Storing Activity/Fragment references (memory leak)
- ❌ GlobalScope instead of viewModelScope
- ❌ No error handling in coroutines
- ❌ Blocking calls with `runBlocking`

**Location:** `app/src/main/java/dev/kamikaze/movike/presentation/ui/viewmodel/FeedViewModel.kt`

### 4. **ApiModule.kt** - Security Issues
- ❌ Logging full API key in logs
- ❌ Logging response body (PII exposure)
- ❌ Using HTTP instead of HTTPS
- ❌ Missing certificate pinning (MITM vulnerability)
- ❌ No hostname verification

**Location:** `app/src/main/java/dev/kamikaze/movike/api/ApiModule.kt`

### 5. **FeedFragment.kt** - Code Style Violations
- ❌ Wrong naming: `IS_LOADING` (UPPER_CASE), `retry_count` (snake_case)
- ❌ Magic numbers: 300, 500, 1000, 16, 42
- ❌ Function naming: `PerformNetworkCall()` (PascalCase)
- ❌ Inconsistent spacing and indentation
- ❌ Dead code: `unusedFunction()`

**Location:** `app/src/main/java/dev/kamikaze/movike/presentation/ui/fragments/FeedFragment.kt`

## Understanding the Output

### Report Structure

```
# 🤖 AI Code Review

**Base branch:** sketch
**Head branch:** current-branch
**Files changed:** 5

---

## 📄 `path/to/file.kt`

**Status:** M (Modified)

### ⚠️ Проблемы:
- Line 42: Issue description

### 🐛 Потенциальные баги:
- Line 15: Potential bug description

### 💡 Советы по улучшению:
- Line 22: Suggestion

### 📚 Связанная документация:
- Related docs from RAG

---

## 📊 Сводка
- **Всего проблем:** X
- **Потенциальных багов:** Y
- **Предложений по улучшению:** Z
```

### Severity Levels

- 🔴 **Critical** - Must fix before merge (security, crashes)
- 🟠 **High** - Should fix before merge (memory leaks, blocking)
- 🟡 **Medium** - Should address (error handling, architecture)
- 🔵 **Low** - Nice to have (style, conventions)

## Advanced Usage

### Check Specific Files

```bash
cd /Users/admin/StudioProjects/movike
python3 assistant/code_reviewer.py sketch
```

### Check Against Different Branch

```bash
python3 assistant/code_reviewer.py main
```

### View Output File

The review is saved to `assistant/review_output.md`:

```bash
cat assistant/review_output.md
```

Or open in your editor:
```bash
open assistant/review_output.md  # macOS
code assistant/review_output.md  # VS Code
```

## How It Works

### 1. RAG System for Context

The reviewer uses RAG (Retrieval-Augmented Generation) to:
- Load 150 documents (documentation + code)
- Find related documentation for each file
- Provide context-aware suggestions

**RAG Index Location:** `assistant/rag_index.json`

### 2. MCP for Git Operations

Uses MCP (Model Context Protocol) to:
- Get list of changed files
- Get diffs between branches
- Read file contents

**MCP Server:** `assistant/mcp_git_server.py`

### 3. Code Analysis

Checks for:
- **Security**: Hardcoded secrets, insecure connections, logging sensitive data
- **Memory**: Leaks, unclosed resources, GlobalScope
- **Architecture**: Blocking calls, wrong dispatchers, DI violations
- **Style**: Naming, magic numbers, formatting, dead code

## Example Output

```
============================================================
  🤖 AI Code Reviewer для Pull Requests
============================================================

📊 Получение информации о PR...

🔍 Анализ изменений...

  Анализирую: app/src/main/java/dev/kamikaze/movike/api/ApiService.kt
  Анализирую: app/src/main/java/dev/kamikaze/movike/repository/RepositoryImpl.kt
  ...

# 🤖 AI Code Review

**Files changed:** 5

## 📄 `ApiService.kt`

### ⚠️ Проблемы:
- Line 14: Использование !! (force unwrap) может привести к NPE
- Line 31: Hardcoded API key found

### 🐛 Потенциальные баги:
- Line 31: Использование GlobalScope - рассмотрите lifecycleScope

## 📊 Сводка
- **Всего проблем:** 12
- **Потенциальных багов:** 8
- **Предложений по улучшению:** 5

### ❗ Рекомендация: Критические проблемы требуют внимания!
```

## GitHub Actions Integration

The code reviewer can run automatically on pull requests.

### Workflow File

Located at: `.github/workflows/code-review.yml`

### Manual Trigger

You can also run it manually:
1. Go to GitHub Actions
2. Select "AI Code Review" workflow
3. Click "Run workflow"

### Environment Variables

For CI/CD:
- `GITHUB_BASE_REF` - Base branch (set by GitHub)
- `GITHUB_STEP_SUMMARY` - Where to save summary (set by GitHub)

## Troubleshooting

### "RAG index not found"

Reindex the project:
```bash
python3 assistant/assistant.py reindex
```

### "No modified files found"

Make sure you have uncommitted changes or compare to correct branch:
```bash
git status
git diff sketch --name-only
```

### "Import error"

Install dependencies:
```bash
cd assistant
pip3 install -r requirements.txt
```

## Summary

**To check all files with intentional errors:**

```bash
cd /Users/admin/StudioProjects/movike
python3 assistant/code_reviewer.py sketch
cat assistant/review_output.md
```

The reviewer will find all the intentional errors we added across 5 files, categorized by:
- Security issues (ApiModule.kt, ApiService.kt)
- Memory leaks (RepositoryImpl.kt, FeedViewModel.kt)
- Code style violations (FeedFragment.kt)
- Architecture problems (all files)

**Expected result:** ~20-30 issues detected across all files.
