#!/usr/bin/env python3
"""
Тестовый клиент для Support Service API
Демонстрирует использование REST API
"""

import requests
import json
import sys


class SupportServiceClient:
    """Клиент для работы с Support Service API"""

    def __init__(self, base_url='http://localhost:5001'):
        self.base_url = base_url

    def health_check(self):
        """Проверка работоспособности сервиса"""
        response = requests.get(f'{self.base_url}/health')
        return response.json()

    def ask_question(self, question, email=None):
        """Задать вопрос ассистенту"""
        data = {'question': question}
        if email:
            data['email'] = email

        response = requests.post(
            f'{self.base_url}/api/support/ask',
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        return response.json()

    def get_user(self, email):
        """Получить информацию о пользователе"""
        response = requests.get(f'{self.base_url}/api/users/{email}')
        return response.json()

    def get_user_tickets(self, user_id):
        """Получить тикеты пользователя"""
        response = requests.get(f'{self.base_url}/api/users/{user_id}/tickets')
        return response.json()

    def get_ticket(self, ticket_id):
        """Получить детали тикета"""
        response = requests.get(f'{self.base_url}/api/tickets/{ticket_id}')
        return response.json()

    def search_tickets(self, keyword):
        """Поиск тикетов по ключевому слову"""
        response = requests.post(
            f'{self.base_url}/api/tickets/search',
            json={'keyword': keyword},
            headers={'Content-Type': 'application/json'}
        )
        return response.json()

    def search_documentation(self, query, limit=3):
        """Поиск в документации"""
        response = requests.post(
            f'{self.base_url}/api/documentation/search',
            json={'query': query, 'limit': limit},
            headers={'Content-Type': 'application/json'}
        )
        return response.json()

    def get_stats(self):
        """Получить статистику системы"""
        response = requests.get(f'{self.base_url}/api/stats')
        return response.json()


def print_separator(title=""):
    """Печать разделителя"""
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print('='*60)
    else:
        print('-'*60)


def pretty_print(data):
    """Красивая печать JSON"""
    print(json.dumps(data, ensure_ascii=False, indent=2))


def main():
    """Главная функция"""
    if len(sys.argv) < 2:
        print("Использование:")
        print("  python3 test_service.py <base_url>")
        print("\nПример:")
        print("  python3 test_service.py http://localhost:5001")
        print("\nИли просто:")
        print("  python3 test_service.py test")
        return

    base_url = sys.argv[1] if sys.argv[1] != 'test' else 'http://localhost:5001'
    client = SupportServiceClient(base_url)

    print("\n" + "="*60)
    print("🎬 MOVIKE SUPPORT SERVICE - TEST CLIENT")
    print("="*60)
    print(f"\n🌐 Подключение к: {base_url}\n")

    try:
        # Тест 1: Health check
        print_separator("ТЕСТ 1: Health Check")
        health = client.health_check()
        pretty_print(health)

        # Тест 2: Статистика системы
        print_separator("ТЕСТ 2: Статистика системы")
        stats = client.get_stats()
        pretty_print(stats)

        # Тест 3: Поиск в документации
        print_separator("ТЕСТ 3: Поиск в документации")
        print("Запрос: 'как восстановить пароль'\n")
        docs = client.search_documentation("как восстановить пароль", limit=2)
        print(f"Найдено результатов: {docs['count']}\n")
        for i, result in enumerate(docs['results'], 1):
            print(f"{i}. Файл: {result['file']}")
            print(f"   Score: {result['score']}")
            preview = result['content'][:100].replace('\n', ' ')
            print(f"   Превью: {preview}...\n")

        # Тест 4: Получение информации о пользователе
        print_separator("ТЕСТ 4: Информация о пользователе")
        user_email = "ivan.petrov@example.com"
        print(f"Email: {user_email}\n")
        user = client.get_user(user_email)
        pretty_print(user)

        # Тест 5: Тикеты пользователя
        print_separator("ТЕСТ 5: Тикеты пользователя")
        user_id = user['user_id']
        print(f"User ID: {user_id}\n")
        tickets = client.get_user_tickets(user_id)
        print(f"Найдено тикетов: {tickets['count']}\n")
        for ticket in tickets['tickets']:
            print(f"• {ticket['ticket_id']}: {ticket['subject']}")
            print(f"  Статус: {ticket['status']} | Приоритет: {ticket['priority']}\n")

        # Тест 6: Поиск тикетов по ключевому слову
        print_separator("ТЕСТ 6: Поиск тикетов")
        keyword = "авторизация"
        print(f"Ключевое слово: '{keyword}'\n")
        search_results = client.search_tickets(keyword)
        print(f"Найдено тикетов: {search_results['count']}\n")
        for ticket in search_results['tickets']:
            print(f"• {ticket['ticket_id']}: {ticket['subject']}")
            print(f"  Категория: {ticket['category']} | Статус: {ticket['status']}\n")

        # Тест 7: Детали тикета
        print_separator("ТЕСТ 7: Детали тикета")
        ticket_id = "TICK-001"
        print(f"Ticket ID: {ticket_id}\n")
        ticket_details = client.get_ticket(ticket_id)
        print(f"Пользователь: {ticket_details['user']['name']}")
        print(f"Тема: {ticket_details['ticket']['subject']}")
        print(f"Статус: {ticket_details['ticket']['status']}")
        print(f"Приоритет: {ticket_details['ticket']['priority']}")
        if 'context' in ticket_details['ticket']:
            print(f"Контекст: {json.dumps(ticket_details['ticket']['context'], ensure_ascii=False)}")

        # Тест 8: Вопрос без контекста пользователя
        print_separator("ТЕСТ 8: Вопрос без контекста")
        question = "Как отменить подписку?"
        print(f"Вопрос: '{question}'\n")
        answer = client.ask_question(question)
        print(f"Уверенность: {answer['confidence']}")
        print(f"\nОтвет:\n{answer['answer'][:500]}...")

        # Тест 9: Вопрос с контекстом пользователя
        print_separator("ТЕСТ 9: Вопрос с контекстом пользователя")
        question = "Почему не работает авторизация?"
        email = "ivan.petrov@example.com"
        print(f"Вопрос: '{question}'")
        print(f"Email: {email}\n")
        answer = client.ask_question(question, email)
        print(f"Уверенность: {answer['confidence']}")
        print(f"\nНайдено в документации: {len(answer['sources']['documentation'])} результатов")
        print(f"Найдено похожих тикетов: {len(answer['sources']['related_tickets'])}")
        if answer['sources']['user_context']:
            user_ctx = answer['sources']['user_context']
            print(f"\nКонтекст пользователя:")
            print(f"  Имя: {user_ctx['name']}")
            print(f"  Подписка: {user_ctx['subscription']}")
            print(f"  Устройство: {user_ctx['device']}")

        print("\n" + "="*60)
        print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ УСПЕШНО")
        print("="*60 + "\n")

    except requests.exceptions.ConnectionError:
        print("\n❌ ОШИБКА: Не удалось подключиться к сервису")
        print(f"\nУбедитесь, что сервис запущен на {base_url}")
        print("Для запуска сервиса используйте:")
        print("  python3 support_service.py\n")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ ОШИБКА: {e}\n")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
