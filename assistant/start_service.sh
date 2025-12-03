#!/bin/bash
# Скрипт для запуска Support Service

echo "═══════════════════════════════════════════════════════════════════"
echo "  🎬 MOVIKE SUPPORT SERVICE - STARTUP"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

# Проверяем наличие виртуального окружения
if [ ! -d "venv" ]; then
    echo "⚠️  Виртуальное окружение не найдено"
    echo ""
    echo "Сначала выполните установку:"
    echo "  ./setup_service.sh"
    echo ""
    echo "Или вручную:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install Flask flask-cors"
    echo ""
    exit 1
fi

# Активируем виртуальное окружение
echo "🔄 Активация виртуального окружения..."
source venv/bin/activate

# Проверяем Flask
if ! python -c "import flask" 2>/dev/null; then
    echo "⚠️  Flask не установлен в виртуальном окружении"
    echo ""
    echo "Установите зависимости:"
    echo "  source venv/bin/activate"
    echo "  pip install Flask flask-cors"
    echo ""
    exit 1
fi

echo "✅ Flask найден"
echo ""

# Проверяем, проиндексирована ли документация
if [ ! -f "rag_index.json" ]; then
    echo "📚 Индексация документации..."
    python support_assistant.py index
    echo ""
fi

# Запускаем сервис
echo "🚀 Запуск Support Service..."
echo ""
python support_service.py "$@"
