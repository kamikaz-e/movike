#!/bin/bash
# Script to set up Git post-commit hook for build time tracking

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
HOOK_FILE="$PROJECT_ROOT/.git/hooks/post-commit"

echo "🔧 Setting up Git post-commit hook for build time tracking..."
echo ""

# Create the hook file
cat > "$HOOK_FILE" << 'EOF'
#!/bin/bash
# Post-commit hook to measure build time and track statistics

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && cd ../.. && pwd )"

echo ""
echo "=================================================="
echo "🔄 Post-commit hook: Build time measurement"
echo "=================================================="
echo ""

# Run the build measurement script
"$SCRIPT_DIR/assistant/measure_build.sh"

echo ""
echo "=================================================="
echo "✅ Build statistics updated!"
echo "=================================================="
echo ""
EOF

# Make the hook executable
chmod +x "$HOOK_FILE"

echo "✅ Post-commit hook installed successfully!"
echo ""
echo "Location: $HOOK_FILE"
echo ""
echo "ℹ️  The hook will automatically run after each commit and:"
echo "   1. Build the project"
echo "   2. Measure the build time"
echo "   3. Update build statistics"
echo "   4. Display current statistics"
echo ""
echo "To disable: Remove or rename the hook file"
echo "To view stats: Run 'python3 assistant/build_stats.py --show'"
echo ""
