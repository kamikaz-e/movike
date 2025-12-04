#!/usr/bin/env python3
"""
Пример интеграции Support Service с ботом
Показывает, как бот может использовать REST API
"""

import json


class MockSupportAPI:
    """
    Мок Support API для демонстрации
    В реальности используйте requests для HTTP запросов
    """

    def __init__(self):
        # Импортируем Support Assistant напрямую для демонстрации
        from support_assistant import SupportAssistant
        self.assistant = SupportAssistant()

    def ask(self, question, email=None):
        """Имитация POST /api/support/ask"""
        result = self.assistant.answer_question(question, email)
        return result


class SupportBot:
    """Пример бота поддержки"""

    def __init__(self, api_url='http://localhost:5001'):
        # В реальности используйте requests
        # self.api = requests (для HTTP запросов)
        # Для демо используем мок
        self.api = MockSupportAPI()

    def handle_message(self, user_message, user_email=None):
        """Обработка сообщения от пользователя"""
        print(f"\n{'='*60}")
        print(f"👤 Пользователь: {user_email or 'Аноним'}")
        print(f"💬 Сообщение: {user_message}")
        print('='*60)

        # Отправляем запрос в Support Service
        try:
            result = self.api.ask(user_message, user_email)

            # Формируем ответ бота
            bot_response = self._format_response(result)

            print(f"\n🤖 БОТ ОТВЕЧАЕТ:\n")
            print(bot_response)

            # Показываем метаданные
            self._show_metadata(result)

            return bot_response

        except Exception as e:
            error_message = "Извините, произошла ошибка. Попробуйте позже или обратитесь в поддержку."
            print(f"\n❌ ОШИБКА: {e}")
            print(f"🤖 БОТ ОТВЕЧАЕТ: {error_message}")
            return error_message

    def _format_response(self, result):
        """Форматирование ответа для бота"""
        answer = result['answer']

        # Сокращаем ответ для бота (первые 500 символов)
        if len(answer) > 500:
            answer = answer[:500] + "...\n\n📚 Подробнее читайте в FAQ или обратитесь в поддержку."

        # Добавляем индикатор уверенности
        confidence_emoji = {
            'high': '✅',
            'medium': '⚠️',
            'low': '❓'
        }
        emoji = confidence_emoji.get(result['confidence'], '❓')

        return f"{answer}\n\n{emoji} Уверенность: {result['confidence']}"

    def _show_metadata(self, result):
        """Показать метаданные ответа (для отладки)"""
        print(f"\n📊 МЕТАДАННЫЕ:")
        print(f"   Уверенность: {result['confidence']}")
        print(f"   Источников документации: {len(result['sources']['documentation'])}")
        print(f"   Похожих тикетов: {len(result['sources']['related_tickets'])}")

        if result['sources']['user_context']:
            user = result['sources']['user_context']
            print(f"   Пользователь: {user['name']} ({user['subscription']})")


def main():
    """Демонстрация работы бота"""
    print("\n" + "="*60)
    print("🤖 MOVIKE SUPPORT BOT - ДЕМОНСТРАЦИЯ")
    print("="*60)
    print("\nПоказываем, как бот использует Support Service API")

    bot = SupportBot()

    # Сценарий 1: Новый пользователь без контекста
    print("\n" + "="*60)
    print("СЦЕНАРИЙ 1: Новый пользователь")
    print("="*60)
    bot.handle_message("Как восстановить пароль?")

    # Сценарий 2: Зарегистрированный пользователь с проблемой
    print("\n" + "="*60)
    print("СЦЕНАРИЙ 2: Пользователь с проблемой авторизации")
    print("="*60)
    bot.handle_message(
        "Не могу войти в приложение, пишет Invalid credentials",
        user_email="ivan.petrov@example.com"
    )

    # Сценарий 3: Вопрос о подписке
    print("\n" + "="*60)
    print("СЦЕНАРИЙ 3: Вопрос о подписке")
    print("="*60)
    bot.handle_message(
        "Как отменить подписку?",
        user_email="maria.sokolova@example.com"
    )

    # Сценарий 4: Технический вопрос
    print("\n" + "="*60)
    print("СЦЕНАРИЙ 4: Технический вопрос")
    print("="*60)
    bot.handle_message(
        "Приложение крашится при использовании поиска",
        user_email="ivan.petrov@example.com"
    )

    print("\n" + "="*60)
    print("✅ ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")
    print("="*60)
    print("\nТак выглядит интеграция Support Service с ботом:")
    print("1. Бот получает сообщение от пользователя")
    print("2. Бот отправляет POST запрос к /api/support/ask")
    print("3. Support Service обрабатывает через RAG + контекст")
    print("4. Бот получает готовый ответ и отправляет пользователю")
    print("\nВ production используйте HTTP запросы через requests:")
    print("  response = requests.post('http://localhost:5001/api/support/ask', ...)")
    print("")


if __name__ == '__main__':
    main()
