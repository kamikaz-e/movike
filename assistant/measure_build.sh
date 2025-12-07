#!/bin/bash
# Script to measure build time and track statistics

set -e

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Get Git information
COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "unknown")
BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "unknown")

echo "=================================================="
echo "🏗️  BUILD TIME MEASUREMENT"
echo "=================================================="
echo "📦 Project: Movike"
echo "🔖 Commit:  $COMMIT_HASH"
echo "🌿 Branch:  $BRANCH"
echo "=================================================="
echo ""

# Record start time
START_TIME=$(date +%s)

# Run the build
echo "🚀 Starting build..."
cd "$PROJECT_ROOT"

# Execute Gradle build
if ./gradlew build; then
    BUILD_SUCCESS=true
    echo ""
    echo "✅ Build completed successfully!"
else
    BUILD_SUCCESS=false
    echo ""
    echo "❌ Build failed!"
fi

# Record end time
END_TIME=$(date +%s)

# Calculate duration
DURATION=$((END_TIME - START_TIME))

echo ""
echo "⏱️  Build duration: ${DURATION} seconds"
echo ""

# Track the build statistics
cd "$SCRIPT_DIR"
python3 build_stats.py "$DURATION" "$COMMIT_HASH" "$BRANCH"

exit 0
