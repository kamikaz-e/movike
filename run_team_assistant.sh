#!/bin/bash
# Team Assistant Service Launcher

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "🤖 Starting Team Assistant Service..."
echo "=================================="
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found. Please install Python 3.7 or higher."
    exit 1
fi

# Check Flask installation
if ! python3 -c "import flask" &> /dev/null; then
    echo "📦 Installing Flask..."
    pip3 install flask flask-cors
fi

# Index documentation first
echo "📚 Indexing documentation..."
cd assistant
python3 simple_rag.py index

# Start the service
echo ""
echo "🚀 Starting service on http://localhost:5001"
echo "=================================="
echo ""
echo "Available endpoints:"
echo "  POST /api/assistant/ask       - Ask questions"
echo "  GET  /api/assistant/status    - Get project status"
echo "  POST /api/tasks/query         - Query tasks"
echo "  POST /api/tasks/create        - Create task"
echo "  GET  /api/rag/search          - Search docs"
echo "  GET  /api/git/context         - Get git info"
echo ""
echo "Note: Port 5001 is used instead of 5001 because macOS AirPlay uses port 5001"
echo "Press Ctrl+C to stop"
echo "=================================="
echo ""

python3 team_assistant_service.py --host 0.0.0.0 --port 5001 --load-samples --debug
