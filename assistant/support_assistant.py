#!/usr/bin/env python3
"""
User Support Assistant
Мини-сервис для ответов на вопросы пользователей о продукте Movike
Использует RAG для поиска в документации/FAQ и JSON с данными пользователей/тикетов
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from simple_rag import SimpleRAG


class SupportAssistant:
    """Ассистент технической поддержки"""

    def __init__(self):
        self.assistant_dir = Path(__file__).parent
        self.crm_data_path = self.assistant_dir / "crm_data.json"

        # Инициализация RAG системы
        self.rag = SimpleRAG()

        # Загрузка данных CRM
        self.load_crm_data()

        print("✓ Support Assistant инициализирован", file=sys.stderr)
        print(f"✓ Загружено пользователей: {len(self.users)}", file=sys.stderr)
        print(f"✓ Загружено тикетов: {len(self.tickets)}", file=sys.stderr)

    def load_crm_data(self):
        """Загружает данные пользователей и тикетов из JSON"""
        if self.crm_data_path.exists():
            with open(self.crm_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.users = data.get('users', [])
                self.tickets = data.get('tickets', [])
        else:
            # Создаем простые тестовые данные
            self.users = [
                {
                    "user_id": "user_001",
                    "email": "ivan.petrov@example.com",
                    "name": "Иван Петров",
                    "subscription": "premium",
                    "device": "Samsung Galaxy S21, Android 13",
                    "app_version": "2.3.1"
                },
                {
                    "user_id": "user_002",
                    "email": "maria.sokolova@example.com",
                    "name": "Мария Соколова",
                    "subscription": "free",
                    "device": "Google Pixel 6, Android 14",
                    "app_version": "2.3.1"
                }
            ]

            self.tickets = [
                {
                    "ticket_id": "TICK-001",
                    "user_id": "user_001",
                    "email": "ivan.petrov@example.com",
                    "category": "auth",
                    "subject": "Не работает авторизация",
                    "description": "При попытке войти появляется ошибка 'Invalid credentials', пароль точно правильный. Письмо для сброса не приходит.",
                    "status": "in_progress",
                    "priority": "high",
                    "created_at": "2024-12-01T10:30:00",
                    "context": {
                        "error_code": "AUTH_001",
                        "last_successful_login": "2024-11-25T08:00:00",
                        "failed_attempts": 5,
                        "email_verified": True
                    }
                },
                {
                    "ticket_id": "TICK-002",
                    "user_id": "user_002",
                    "email": "maria.sokolova@example.com",
                    "category": "payment",
                    "subject": "Не прошел платеж за премиум",
                    "description": "Деньги списались с карты, но подписка не активировалась. Прошло уже 2 часа.",
                    "status": "resolved",
                    "priority": "urgent",
                    "created_at": "2024-11-28T15:45:00",
                    "resolved_at": "2024-11-28T18:30:00",
                    "context": {
                        "payment_id": "PAY_12345",
                        "amount": "299.00 RUB",
                        "payment_method": "card",
                        "transaction_status": "pending_confirmation"
                    }
                },
                {
                    "ticket_id": "TICK-003",
                    "user_id": "user_001",
                    "email": "ivan.petrov@example.com",
                    "category": "technical",
                    "subject": "Приложение вылетает при поиске",
                    "description": "Каждый раз при использовании поиска приложение закрывается. Samsung Galaxy S21, Android 13.",
                    "status": "open",
                    "priority": "medium",
                    "created_at": "2024-12-02T09:15:00",
                    "context": {
                        "crash_count": 3,
                        "last_crash": "2024-12-02T09:10:00",
                        "search_query": "interstellar"
                    }
                }
            ]

            # Сохраняем тестовые данные
            self.save_crm_data()

    def save_crm_data(self):
        """Сохраняет данные в JSON файл"""
        with open(self.crm_data_path, 'w', encoding='utf-8') as f:
            json.dump({
                'users': self.users,
                'tickets': self.tickets
            }, f, ensure_ascii=False, indent=2)

    def find_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Находит пользователя по email"""
        for user in self.users:
            if user['email'].lower() == email.lower():
                return user
        return None

    def find_user_tickets(self, user_id: str) -> List[Dict[str, Any]]:
        """Получает все тикеты пользователя"""
        return [t for t in self.tickets if t['user_id'] == user_id]

    def search_tickets_by_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Поиск тикетов по ключевым словам"""
        keyword_lower = keyword.lower()
        results = []

        for ticket in self.tickets:
            if (keyword_lower in ticket['subject'].lower() or
                keyword_lower in ticket['description'].lower() or
                keyword_lower in ticket['category'].lower()):
                results.append(ticket)

        return results

    def get_ticket_context(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Получает полный контекст тикета"""
        for ticket in self.tickets:
            if ticket['ticket_id'] == ticket_id:
                # Получаем информацию о пользователе
                user = None
                for u in self.users:
                    if u['user_id'] == ticket['user_id']:
                        user = u
                        break

                return {
                    "ticket": ticket,
                    "user": user
                }
        return None

    def search_documentation(self, query: str) -> List[Dict[str, Any]]:
        """Поиск в документации через RAG"""
        return self.rag.search(query, limit=3)

    def answer_question(self, question: str, user_email: Optional[str] = None) -> Dict[str, Any]:
        """
        Главный метод для ответа на вопросы пользователей
        Комбинирует RAG (документация) и контекст пользователя/тикетов
        """
        response = {
            "question": question,
            "answer": "",
            "sources": {
                "documentation": [],
                "user_context": None,
                "related_tickets": []
            },
            "confidence": "medium"
        }

        # 1. Поиск в документации через RAG
        doc_results = self.search_documentation(question)
        response["sources"]["documentation"] = doc_results

        # 2. Если указан email, получаем контекст пользователя
        if user_email:
            user = self.find_user_by_email(user_email)
            if user:
                response["sources"]["user_context"] = user

                # Получаем тикеты пользователя
                user_tickets = self.find_user_tickets(user['user_id'])
                response["sources"]["related_tickets"] = user_tickets

        # 3. Поиск похожих тикетов по ключевым словам
        keywords = question.lower().split()
        for keyword in ['авторизация', 'платеж', 'вылетает', 'не работает', 'ошибка']:
            if keyword in question.lower():
                similar_tickets = self.search_tickets_by_keyword(keyword)
                response["sources"]["related_tickets"].extend(similar_tickets)

        # Убираем дубликаты тикетов
        seen_ids = set()
        unique_tickets = []
        for ticket in response["sources"]["related_tickets"]:
            if ticket['ticket_id'] not in seen_ids:
                seen_ids.add(ticket['ticket_id'])
                unique_tickets.append(ticket)
        response["sources"]["related_tickets"] = unique_tickets

        # 4. Формируем ответ на основе найденной информации
        response["answer"] = self.generate_answer(question, response["sources"])

        # 5. Определяем уверенность ответа
        if doc_results and len(doc_results) > 0:
            response["confidence"] = "high"
        elif response["sources"]["related_tickets"]:
            response["confidence"] = "medium"
        else:
            response["confidence"] = "low"

        return response

    def generate_answer(self, question: str, sources: Dict[str, Any]) -> str:
        """Генерирует ответ на основе найденных источников"""
        answer_parts = []

        # Информация из документации
        if sources["documentation"]:
            answer_parts.append("📚 ИЗ ДОКУМЕНТАЦИИ:\n")
            for i, doc in enumerate(sources["documentation"][:3], 1):
                answer_parts.append(f"{i}. Файл: {doc['file']}")
                if 'score' in doc:
                    answer_parts.append(f"   Релевантность: {doc['score']}")
                answer_parts.append(f"\n   Содержимое:")
                answer_parts.append("   " + "-" * 56)
                
                # Форматируем содержимое с переносами строк
                content_lines = doc['content'].split('\n')
                non_empty_lines = [line for line in content_lines if line.strip()]
                
                shown_count = 0
                for line in non_empty_lines[:12]:  # Показываем первые 12 непустых строк
                    # Обрезаем слишком длинные строки (макс 75 символов)
                    if len(line) > 75:
                        line = line[:72] + "..."
                    answer_parts.append(f"   {line}")
                    shown_count += 1
                
                if len(non_empty_lines) > shown_count:
                    answer_parts.append(f"   ... ({len(non_empty_lines) - shown_count} строк скрыто)")
                
                answer_parts.append("   " + "-" * 56)
                answer_parts.append("")

        # Контекст пользователя
        if sources["user_context"]:
            user = sources["user_context"]
            answer_parts.append(f"\n👤 ВАШИ ДАННЫЕ:")
            answer_parts.append(f"   Имя: {user['name']}")
            answer_parts.append(f"   Подписка: {user['subscription']}")
            answer_parts.append(f"   Устройство: {user['device']}")
            answer_parts.append(f"   Версия приложения: {user['app_version']}\n")

        # Похожие тикеты
        if sources["related_tickets"]:
            answer_parts.append(f"\n🎫 ПОХОЖИЕ ОБРАЩЕНИЯ (найдено: {len(sources['related_tickets'])}):\n")
            for ticket in sources["related_tickets"][:3]:
                answer_parts.append(f"• {ticket['ticket_id']}: {ticket['subject']}")
                answer_parts.append(f"  Статус: {ticket['status']} | Приоритет: {ticket['priority']}")
                
                # Описание тикета с переносами строк
                if ticket.get('description'):
                    desc_text = ticket['description']
                    # Обрезаем слишком длинное описание
                    if len(desc_text) > 150:
                        desc_text = desc_text[:147] + "..."
                    # Разбиваем на строки, но показываем компактно
                    desc_lines = desc_text.split('\n')
                    if len(desc_lines) == 1:
                        answer_parts.append(f"  Описание: {desc_lines[0]}")
                    else:
                        answer_parts.append(f"  Описание:")
                        for desc_line in desc_lines[:2]:  # Первые 2 строки
                            if desc_line.strip():
                                if len(desc_line) > 70:
                                    desc_line = desc_line[:67] + "..."
                                answer_parts.append(f"    {desc_line}")
                        if len(desc_lines) > 2:
                            answer_parts.append(f"    ...")

                if ticket.get('context'):
                    context_info = []
                    ctx = ticket['context']

                    if 'error_code' in ctx:
                        context_info.append(f"Код ошибки: {ctx['error_code']}")
                    if 'failed_attempts' in ctx:
                        context_info.append(f"Неудачных попыток: {ctx['failed_attempts']}")
                    if 'payment_id' in ctx:
                        context_info.append(f"ID платежа: {ctx['payment_id']}")
                    if 'crash_count' in ctx:
                        context_info.append(f"Крашей: {ctx['crash_count']}")

                    if context_info:
                        context_str = ', '.join(context_info)
                        if len(context_str) > 70:
                            context_str = context_str[:67] + "..."
                        answer_parts.append(f"  Контекст: {context_str}")

                answer_parts.append("")

        # Если ничего не найдено
        if not answer_parts:
            answer_parts.append("❌ К сожалению, не удалось найти информацию по вашему вопросу.")
            answer_parts.append("\nРекомендации:")
            answer_parts.append("• Проверьте FAQ в документации")
            answer_parts.append("• Обратитесь в техподдержку: support@movike.app")
            answer_parts.append("• Создайте новый тикет через приложение")

        return "\n".join(answer_parts)

    def interactive_mode(self):
        """Интерактивный режим работы с ассистентом"""
        print("\n" + "="*60)
        print("🎬 MOVIKE SUPPORT ASSISTANT")
        print("="*60)
        print("\nДобро пожаловать! Я помогу вам с вопросами о приложении Movike.")
        print("\nКоманды:")
        print("  • Введите ваш вопрос")
        print("  • 'user:<email>' - указать email для персонализации")
        print("  • 'ticket:<id>' - посмотреть детали тикета")
        print("  • 'exit' - выход")
        print("="*60 + "\n")

        current_user_email = None

        while True:
            try:
                user_input = input("Вы: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == 'exit':
                    print("\nДо свидания! Хорошего дня!")
                    break

                # Команда: указать email пользователя
                if user_input.lower().startswith('user:'):
                    email = user_input[5:].strip()
                    user = self.find_user_by_email(email)
                    if user:
                        current_user_email = email
                        print(f"\n✓ Пользователь установлен: {user['name']} ({email})")
                        tickets = self.find_user_tickets(user['user_id'])
                        if tickets:
                            print(f"  Активных тикетов: {len(tickets)}")
                    else:
                        print(f"\n✗ Пользователь с email '{email}' не найден")
                    print()
                    continue

                # Команда: детали тикета
                if user_input.lower().startswith('ticket:'):
                    ticket_id = user_input[7:].strip().upper()
                    context = self.get_ticket_context(ticket_id)
                    if context:
                        ticket = context['ticket']
                        user = context['user']
                        print(f"\n📋 ТИКЕТ {ticket['ticket_id']}")
                        print(f"   Пользователь: {user['name']} ({user['email']})")
                        print(f"   Тема: {ticket['subject']}")
                        print(f"   Категория: {ticket['category']}")
                        print(f"   Статус: {ticket['status']}")
                        print(f"   Приоритет: {ticket['priority']}")
                        print(f"   Описание: {ticket['description']}")
                        if ticket.get('context'):
                            print(f"   Контекст: {json.dumps(ticket['context'], ensure_ascii=False, indent=6)}")
                    else:
                        print(f"\n✗ Тикет '{ticket_id}' не найден")
                    print()
                    continue

                # Обычный вопрос
                print("\n🤔 Обрабатываю ваш вопрос...\n")

                result = self.answer_question(user_input, current_user_email)

                print("="*60)
                print(result['answer'])
                print("="*60)
                print(f"\n💡 Уверенность: {result['confidence']}")
                print()

            except KeyboardInterrupt:
                print("\n\nДо свидания!")
                break
            except Exception as e:
                print(f"\n❌ Ошибка: {e}\n")

    def cli_mode(self, question: str, user_email: Optional[str] = None):
        """Режим командной строки для одного вопроса"""
        result = self.answer_question(question, user_email)

        print("\n" + "="*60)
        print("🎬 MOVIKE SUPPORT ASSISTANT")
        print("="*60)
        print(f"\nВопрос: {question}")
        if user_email:
            print(f"Пользователь: {user_email}")
        print("\n" + "-"*60)
        print(result['answer'])
        print("-"*60)
        print(f"\n💡 Уверенность ответа: {result['confidence']}")
        print()


def main():
    """Главная функция"""
    assistant = SupportAssistant()

    if len(sys.argv) > 1:
        # Режим CLI с параметрами
        command = sys.argv[1]

        if command == "ask":
            # python3 support_assistant.py ask "вопрос" [email]
            if len(sys.argv) < 3:
                print("Использование: python3 support_assistant.py ask 'вопрос' [email]")
                return

            question = sys.argv[2]
            user_email = sys.argv[3] if len(sys.argv) > 3 else None
            assistant.cli_mode(question, user_email)

        elif command == "index":
            # Индексация документации
            print("Индексация документации...")
            assistant.rag.index_all()

        elif command == "test":
            # Тестовый режим
            print("\n=== ТЕСТ SUPPORT ASSISTANT ===\n")

            # Тест 1: Вопрос об авторизации
            print("1️⃣ Тест: Вопрос об авторизации с контекстом пользователя")
            result = assistant.answer_question(
                "Почему не работает авторизация?",
                "ivan.petrov@example.com"
            )
            print(f"Найдено источников документации: {len(result['sources']['documentation'])}")
            print(f"Найдено похожих тикетов: {len(result['sources']['related_tickets'])}")
            print(f"Уверенность: {result['confidence']}\n")
            print(result['answer'])
            print("\n" + "="*60 + "\n")

            # Тест 2: Вопрос о платежах
            print("2️⃣ Тест: Вопрос о платежах")
            result = assistant.answer_question(
                "Не прошел платеж за подписку",
                "maria.sokolova@example.com"
            )
            print(f"Найдено источников документации: {len(result['sources']['documentation'])}")
            print(f"Найдено похожих тикетов: {len(result['sources']['related_tickets'])}")
            print(f"Уверенность: {result['confidence']}\n")
            print(result['answer'])
            print("\n" + "="*60 + "\n")

            # Тест 3: Общий вопрос без контекста
            print("3️⃣ Тест: Общий вопрос без контекста пользователя")
            result = assistant.answer_question("Как восстановить пароль?")
            print(f"Найдено источников документации: {len(result['sources']['documentation'])}")
            print(f"Уверенность: {result['confidence']}\n")
            print(result['answer'])

        else:
            print(f"Неизвестная команда: {command}")
            print("\nДоступные команды:")
            print("  python3 support_assistant.py              # Интерактивный режим")
            print("  python3 support_assistant.py ask 'вопрос' [email]")
            print("  python3 support_assistant.py index        # Индексация документации")
            print("  python3 support_assistant.py test         # Тестовый режим")

    else:
        # Интерактивный режим по умолчанию
        assistant.interactive_mode()


if __name__ == "__main__":
    main()
