#!/bin/bash
# Тест создания задачи через API

echo "🧪 Тестирование создания задачи через чат"
echo "=========================================="
echo ""

BASE_URL="http://localhost:5001"

# Тест 1: Создание задачи через ask endpoint
echo "📝 Тест 1: Создание задачи через /api/assistant/ask"
echo "Команда: Create task: Fix memory leak with high priority. Description: Images not released properly"
echo ""

RESPONSE=$(curl -s -X POST "$BASE_URL/api/assistant/ask" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Create task: Fix memory leak with high priority. Description: Images not released properly",
    "context": {
      "includeRAG": false,
      "includeGitContext": false,
      "includeTasks": false
    }
  }')

echo "Ответ сервера:"
echo "$RESPONSE" | python3 -m json.tool 2>/dev/null || echo "$RESPONSE"
echo ""
echo "=========================================="
echo ""

# Тест 2: Проверка созданных задач
echo "📋 Тест 2: Проверка созданных задач"
echo ""

TASKS=$(curl -s -X POST "$BASE_URL/api/tasks/query" \
  -H "Content-Type: application/json" \
  -d '{}')

echo "Список задач:"
echo "$TASKS" | python3 -m json.tool 2>/dev/null || echo "$TASKS"
echo ""

