#!/bin/bash
# Test script for Team Assistant

echo "🧪 Testing Team Assistant Service"
echo "=================================="
echo ""

# Start backend in background
echo "📦 Starting backend service..."
./run_team_assistant.sh &
BACKEND_PID=$!

# Wait for service to start
echo "⏳ Waiting for service to start..."
sleep 5

# Health check
echo "✓ Testing health endpoint..."
curl -s http://localhost:5001/health | python3 -m json.tool

echo ""
echo "✓ Testing project status..."
curl -s http://localhost:5001/api/assistant/status | python3 -m json.tool | head -20

echo ""
echo "✓ Testing task query..."
curl -s -X POST http://localhost:5001/api/tasks/query \
  -H "Content-Type: application/json" \
  -d '{"priority": "HIGH"}' | python3 -m json.tool | head -20

echo ""
echo "✓ Testing documentation search..."
curl -s "http://localhost:5001/api/rag/search?query=architecture&limit=2" | python3 -m json.tool | head -20

echo ""
echo "✓ Testing assistant question..."
curl -s -X POST http://localhost:5001/api/assistant/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Show high priority tasks"}' | python3 -m json.tool | head -30

echo ""
echo ""
echo "=================================="
echo "✅ All tests completed!"
echo "=================================="
echo ""
echo "Press Ctrl+C to stop the service"
echo ""

# Keep script running
wait $BACKEND_PID
