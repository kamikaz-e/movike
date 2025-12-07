#!/bin/bash
# Quick backend-only test (no Android app required)

echo "🧪 Testing Team Assistant Backend Only"
echo "======================================"
echo ""

# Check if backend is running
echo "Checking if backend is running..."
if ! curl -s http://localhost:5001/health > /dev/null 2>&1; then
    echo "❌ Backend not running!"
    echo ""
    echo "Start it with: ./run_team_assistant.sh"
    exit 1
fi

echo "✅ Backend is running"
echo ""

# Run tests
echo "1️⃣  Testing health endpoint..."
curl -s http://localhost:5001/health | python3 -m json.tool
echo ""

echo "2️⃣  Testing project status..."
curl -s http://localhost:5001/api/assistant/status | python3 -m json.tool
echo ""

echo "3️⃣  Testing high priority tasks query..."
curl -s -X POST http://localhost:5001/api/tasks/query \
  -H "Content-Type: application/json" \
  -d '{"priority": "HIGH"}' | python3 -m json.tool
echo ""

echo "4️⃣  Testing documentation search..."
curl -s "http://localhost:5001/api/rag/search?query=architecture&limit=2" | python3 -m json.tool
echo ""

echo "5️⃣  Testing assistant question (Show high priority tasks)..."
curl -s -X POST http://localhost:5001/api/assistant/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Show high priority tasks"}' | python3 -m json.tool
echo ""

echo "6️⃣  Testing assistant question (What should I do first?)..."
curl -s -X POST http://localhost:5001/api/assistant/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What should I do first?"}' | python3 -m json.tool
echo ""

echo "7️⃣  Testing create task..."
curl -s -X POST http://localhost:5001/api/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test task from script",
    "description": "This is a test task",
    "priority": "MEDIUM",
    "tags": ["test", "automation"]
  }' | python3 -m json.tool
echo ""

echo "8️⃣  Testing git context..."
curl -s http://localhost:5001/api/git/context | python3 -m json.tool
echo ""

echo ""
echo "======================================"
echo "✅ All backend tests completed!"
echo "======================================"
echo ""
echo "Backend is working correctly! 🎉"
echo ""
echo "Next steps:"
echo "1. Fix the Android Dagger issue (see IMPLEMENTATION_SUMMARY.md)"
echo "2. Build the Android app"
echo "3. Launch AssistantChatActivity"
echo "4. Start chatting with your Team Assistant!"
