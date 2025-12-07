#!/bin/bash
# Настройка и запуск Support Service с виртуальным окружением

echo "═══════════════════════════════════════════════════════════════════"
echo "  🎬 MOVIKE SUPPORT SERVICE - SETUP"
echo "═══════════════════════════════════════════════════════════════════"
echo ""

cd "$(dirname "$0")"

# Проверяем наличие виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv

    if [ $? -ne 0 ]; then
        echo "❌ Ошибка создания виртуального окружения"
        exit 1
    fi

    echo "✅ Виртуальное окружение создано"
    echo ""
fi

# Активируем виртуальное окружение
echo "🔄 Активация виртуального окружения..."
source venv/bin/activate

# Проверяем установлен ли Flask
if ! python -c "import flask" 2>/dev/null; then
    echo "📥 Установка зависимостей..."
    pip install Flask flask-cors gunicorn --quiet

    if [ $? -ne 0 ]; then
        echo "❌ Ошибка установки зависимостей"
        exit 1
    fi

    echo "✅ Зависимости установлены"
    echo ""
fi

# Проверяем индексацию
if [ ! -f "rag_index.json" ]; then
    echo "📚 Индексация документации..."
    python support_assistant.py index
    echo ""
fi

echo "✅ Настройка завершена"
echo ""
echo "Для запуска сервиса используйте:"
echo "  source venv/bin/activate"
echo "  python support_service.py"
echo ""
echo "Или запустите сейчас? [y/N]"
read -r response

if [[ "$response" =~ ^[Yy]$ ]]; then
    echo ""
    python support_service.py
else
    echo ""
    echo "Для запуска позже выполните:"
    echo "  cd $(pwd)"
    echo "  source venv/bin/activate"
    echo "  python support_service.py"
    echo ""
fi
