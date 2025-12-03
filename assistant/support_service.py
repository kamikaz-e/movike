#!/usr/bin/env python3
"""
Support Service - REST API для User Support Assistant
Предоставляет HTTP API для работы с ассистентом поддержки
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
from pathlib import Path
from support_assistant import SupportAssistant

# Инициализация Flask приложения
app = Flask(__name__)
CORS(app)  # Разрешаем CORS для всех доменов

# Инициализация Support Assistant
print("🚀 Инициализация Support Assistant...", file=sys.stderr)
assistant = SupportAssistant()
print("✅ Support Assistant готов к работе\n", file=sys.stderr)


@app.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервиса"""
    return jsonify({
        'status': 'ok',
        'service': 'Movike Support Assistant',
        'version': '1.0.0'
    })


@app.route('/api/support/ask', methods=['POST'])
def ask_question():
    """
    Задать вопрос ассистенту

    Request body:
    {
        "question": "Почему не работает авторизация?",
        "email": "user@example.com"  // опционально
    }

    Response:
    {
        "question": "...",
        "answer": "...",
        "sources": {
            "documentation": [...],
            "user_context": {...},
            "related_tickets": [...]
        },
        "confidence": "high|medium|low"
    }
    """
    try:
        data = request.get_json()

        if not data or 'question' not in data:
            return jsonify({
                'error': 'Missing required field: question'
            }), 400

        question = data['question']
        email = data.get('email')

        # Получаем ответ от ассистента
        result = assistant.answer_question(question, email)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/users/<email>', methods=['GET'])
def get_user(email):
    """
    Получить информацию о пользователе по email

    Response:
    {
        "user_id": "user_001",
        "email": "...",
        "name": "...",
        "subscription": "...",
        "device": "...",
        "app_version": "..."
    }
    """
    try:
        user = assistant.find_user_by_email(email)

        if user:
            return jsonify(user), 200
        else:
            return jsonify({
                'error': 'User not found'
            }), 404

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/users/<user_id>/tickets', methods=['GET'])
def get_user_tickets(user_id):
    """
    Получить все тикеты пользователя

    Response:
    {
        "user_id": "user_001",
        "tickets": [...],
        "count": 2
    }
    """
    try:
        tickets = assistant.find_user_tickets(user_id)

        return jsonify({
            'user_id': user_id,
            'tickets': tickets,
            'count': len(tickets)
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/tickets/<ticket_id>', methods=['GET'])
def get_ticket(ticket_id):
    """
    Получить детальную информацию о тикете

    Response:
    {
        "ticket": {...},
        "user": {...}
    }
    """
    try:
        context = assistant.get_ticket_context(ticket_id)

        if context:
            return jsonify(context), 200
        else:
            return jsonify({
                'error': 'Ticket not found'
            }), 404

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/tickets/search', methods=['POST'])
def search_tickets():
    """
    Поиск тикетов по ключевым словам

    Request body:
    {
        "keyword": "авторизация"
    }

    Response:
    {
        "keyword": "авторизация",
        "tickets": [...],
        "count": 2
    }
    """
    try:
        data = request.get_json()

        if not data or 'keyword' not in data:
            return jsonify({
                'error': 'Missing required field: keyword'
            }), 400

        keyword = data['keyword']
        tickets = assistant.search_tickets_by_keyword(keyword)

        return jsonify({
            'keyword': keyword,
            'tickets': tickets,
            'count': len(tickets)
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/documentation/search', methods=['POST'])
def search_documentation():
    """
    Поиск в документации через RAG

    Request body:
    {
        "query": "как восстановить пароль",
        "limit": 5  // опционально, по умолчанию 3
    }

    Response:
    {
        "query": "...",
        "results": [
            {
                "file": "project/docs/SUPPORT_FAQ.md",
                "chunk_index": 0,
                "content": "...",
                "score": 10
            }
        ],
        "count": 3
    }
    """
    try:
        data = request.get_json()

        if not data or 'query' not in data:
            return jsonify({
                'error': 'Missing required field: query'
            }), 400

        query = data['query']
        limit = data.get('limit', 3)

        results = assistant.search_documentation(query)[:limit]

        return jsonify({
            'query': query,
            'results': results,
            'count': len(results)
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """
    Получить статистику системы

    Response:
    {
        "users_count": 2,
        "tickets_count": 3,
        "documentation_chunks": 44
    }
    """
    try:
        return jsonify({
            'users_count': len(assistant.users),
            'tickets_count': len(assistant.tickets),
            'documentation_chunks': len(assistant.rag.documents)
        }), 200

    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500


# Главная страница с API документацией
@app.route('/', methods=['GET'])
def index():
    """Главная страница с описанием API"""
    return jsonify({
        'service': 'Movike Support Assistant API',
        'version': '1.0.0',
        'endpoints': {
            'GET /health': 'Проверка работоспособности',
            'POST /api/support/ask': 'Задать вопрос ассистенту',
            'GET /api/users/<email>': 'Получить информацию о пользователе',
            'GET /api/users/<user_id>/tickets': 'Получить тикеты пользователя',
            'GET /api/tickets/<ticket_id>': 'Получить детали тикета',
            'POST /api/tickets/search': 'Поиск тикетов по ключевым словам',
            'POST /api/documentation/search': 'Поиск в документации',
            'GET /api/stats': 'Статистика системы'
        },
        'documentation': 'https://github.com/movike/support-assistant'
    })


def main():
    """Запуск сервиса"""
    import argparse

    parser = argparse.ArgumentParser(description='Movike Support Service')
    parser.add_argument('--host', default='0.0.0.0', help='Host для запуска (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Port для запуска (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Режим отладки')

    args = parser.parse_args()

    print("\n" + "="*60)
    print("🎬 MOVIKE SUPPORT SERVICE")
    print("="*60)
    print(f"\n🌐 Сервис запущен на http://{args.host}:{args.port}")
    print("\n📚 Доступные endpoints:")
    print(f"  • http://{args.host}:{args.port}/health")
    print(f"  • http://{args.host}:{args.port}/api/support/ask")
    print(f"  • http://{args.host}:{args.port}/api/users/<email>")
    print(f"  • http://{args.host}:{args.port}/api/documentation/search")
    print("\n💡 Для просмотра всех endpoints откройте:")
    print(f"  http://{args.host}:{args.port}/")
    print("\n" + "="*60 + "\n")

    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug
    )


if __name__ == '__main__':
    main()
