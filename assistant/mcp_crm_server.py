#!/usr/bin/env python3
"""
MCP сервер для интеграции с CRM (Customer Relationship Management)
Предоставляет доступ к данным пользователей и тикетам поддержки
"""

import json
import sys
from typing import Dict, Any, List, Optional
from pathlib import Path
from datetime import datetime


class CRMMCPServer:
    """MCP сервер для CRM операций"""

    def __init__(self):
        self.assistant_dir = Path(__file__).parent
        self.crm_data_path = self.assistant_dir / "crm_data.json"

        # Загружаем данные CRM
        self.load_crm_data()

        self.tools = {
            "get_user_by_email": {
                "name": "get_user_by_email",
                "description": "Получает информацию о пользователе по email",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "email": {
                            "type": "string",
                            "description": "Email пользователя"
                        }
                    },
                    "required": ["email"]
                }
            },
            "get_user_tickets": {
                "name": "get_user_tickets",
                "description": "Получает все тикеты пользователя",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID пользователя"
                        },
                        "status": {
                            "type": "string",
                            "description": "Фильтр по статусу (open, in_progress, resolved, closed)",
                            "enum": ["open", "in_progress", "resolved", "closed", "all"]
                        }
                    },
                    "required": ["user_id"]
                }
            },
            "get_ticket": {
                "name": "get_ticket",
                "description": "Получает детальную информацию о тикете",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "ticket_id": {
                            "type": "string",
                            "description": "ID тикета"
                        }
                    },
                    "required": ["ticket_id"]
                }
            },
            "search_tickets": {
                "name": "search_tickets",
                "description": "Поиск тикетов по ключевым словам",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Поисковый запрос"
                        },
                        "category": {
                            "type": "string",
                            "description": "Категория тикета",
                            "enum": ["auth", "payment", "technical", "content", "account", "all"]
                        }
                    },
                    "required": ["query"]
                }
            },
            "get_user_subscription": {
                "name": "get_user_subscription",
                "description": "Получает информацию о подписке пользователя",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID пользователя"
                        }
                    },
                    "required": ["user_id"]
                }
            },
            "create_ticket": {
                "name": "create_ticket",
                "description": "Создает новый тикет поддержки",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "user_id": {
                            "type": "string",
                            "description": "ID пользователя"
                        },
                        "category": {
                            "type": "string",
                            "description": "Категория проблемы",
                            "enum": ["auth", "payment", "technical", "content", "account"]
                        },
                        "subject": {
                            "type": "string",
                            "description": "Тема тикета"
                        },
                        "description": {
                            "type": "string",
                            "description": "Описание проблемы"
                        },
                        "priority": {
                            "type": "string",
                            "description": "Приоритет",
                            "enum": ["low", "medium", "high", "urgent"]
                        }
                    },
                    "required": ["user_id", "category", "subject", "description"]
                }
            }
        }

    def load_crm_data(self):
        """Загружает данные CRM из файла"""
        if self.crm_data_path.exists():
            with open(self.crm_data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.users = data.get('users', [])
                self.tickets = data.get('tickets', [])
        else:
            # Создаем тестовые данные
            self.users = [
                {
                    "user_id": "user_001",
                    "email": "ivan.petrov@example.com",
                    "name": "Иван Петров",
                    "phone": "+7 (999) 123-45-67",
                    "registration_date": "2024-01-15",
                    "subscription": {
                        "plan": "premium",
                        "status": "active",
                        "expires": "2025-01-15",
                        "auto_renewal": True
                    },
                    "device": {
                        "model": "Samsung Galaxy S21",
                        "os_version": "Android 13",
                        "app_version": "2.3.1"
                    }
                },
                {
                    "user_id": "user_002",
                    "email": "maria.sokolova@example.com",
                    "name": "Мария Соколова",
                    "phone": "+7 (999) 234-56-78",
                    "registration_date": "2024-03-20",
                    "subscription": {
                        "plan": "free",
                        "status": "active",
                        "expires": None,
                        "auto_renewal": False
                    },
                    "device": {
                        "model": "Google Pixel 6",
                        "os_version": "Android 14",
                        "app_version": "2.3.1"
                    }
                },
                {
                    "user_id": "user_003",
                    "email": "alex.ivanov@example.com",
                    "name": "Алексей Иванов",
                    "phone": "+7 (999) 345-67-89",
                    "registration_date": "2023-11-10",
                    "subscription": {
                        "plan": "family",
                        "status": "active",
                        "expires": "2024-12-31",
                        "auto_renewal": True,
                        "family_members": 4
                    },
                    "device": {
                        "model": "Xiaomi Mi 11",
                        "os_version": "Android 12",
                        "app_version": "2.2.8"
                    }
                }
            ]

            self.tickets = [
                {
                    "ticket_id": "TICK-001",
                    "user_id": "user_001",
                    "category": "auth",
                    "subject": "Не работает авторизация",
                    "description": "При попытке войти в приложение появляется ошибка 'Invalid credentials', хотя пароль точно правильный. Пробовал сбросить пароль, но письмо не приходит.",
                    "status": "in_progress",
                    "priority": "high",
                    "created_at": "2024-12-01T10:30:00",
                    "updated_at": "2024-12-01T14:20:00",
                    "assigned_to": "support_agent_1",
                    "messages": [
                        {
                            "from": "user",
                            "text": "Не могу войти в приложение",
                            "timestamp": "2024-12-01T10:30:00"
                        },
                        {
                            "from": "support",
                            "text": "Проверяем ваш аккаунт. Можете указать email для восстановления?",
                            "timestamp": "2024-12-01T14:20:00"
                        }
                    ]
                },
                {
                    "ticket_id": "TICK-002",
                    "user_id": "user_002",
                    "category": "payment",
                    "subject": "Не прошел платеж за премиум",
                    "description": "Пыталась оплатить премиум подписку, деньги списались с карты, но подписка не активировалась. Прошло уже 2 часа.",
                    "status": "resolved",
                    "priority": "urgent",
                    "created_at": "2024-11-28T15:45:00",
                    "updated_at": "2024-11-28T18:30:00",
                    "resolved_at": "2024-11-28T18:30:00",
                    "assigned_to": "support_agent_2",
                    "resolution": "Платеж был обработан с задержкой. Подписка активирована вручную, деньги возвращены не будут так как услуга предоставлена.",
                    "messages": [
                        {
                            "from": "user",
                            "text": "Деньги списались, а премиума нет!",
                            "timestamp": "2024-11-28T15:45:00"
                        },
                        {
                            "from": "support",
                            "text": "Проверяем платеж. Можете предоставить скриншот списания?",
                            "timestamp": "2024-11-28T16:10:00"
                        },
                        {
                            "from": "user",
                            "text": "[screenshot.jpg]",
                            "timestamp": "2024-11-28T16:15:00"
                        },
                        {
                            "from": "support",
                            "text": "Подписка активирована. Приносим извинения за задержку!",
                            "timestamp": "2024-11-28T18:30:00"
                        }
                    ]
                },
                {
                    "ticket_id": "TICK-003",
                    "user_id": "user_001",
                    "category": "technical",
                    "subject": "Приложение вылетает при поиске",
                    "description": "Каждый раз когда пытаюсь искать фильмы, приложение закрывается. Samsung Galaxy S21, Android 13, версия приложения 2.3.1",
                    "status": "open",
                    "priority": "medium",
                    "created_at": "2024-12-02T09:15:00",
                    "updated_at": "2024-12-02T09:15:00",
                    "assigned_to": None,
                    "messages": [
                        {
                            "from": "user",
                            "text": "Приложение крашится при использовании поиска",
                            "timestamp": "2024-12-02T09:15:00"
                        }
                    ]
                },
                {
                    "ticket_id": "TICK-004",
                    "user_id": "user_003",
                    "category": "content",
                    "subject": "Не загружаются постеры фильмов",
                    "description": "Список фильмов загружается, но вместо постеров показываются серые квадраты. Интернет нормальный, другие приложения работают.",
                    "status": "closed",
                    "priority": "low",
                    "created_at": "2024-11-25T12:00:00",
                    "updated_at": "2024-11-26T10:30:00",
                    "resolved_at": "2024-11-26T10:00:00",
                    "closed_at": "2024-11-26T10:30:00",
                    "assigned_to": "support_agent_1",
                    "resolution": "Проблема была на стороне CDN. Исправлено.",
                    "messages": [
                        {
                            "from": "user",
                            "text": "Не вижу картинки фильмов",
                            "timestamp": "2024-11-25T12:00:00"
                        },
                        {
                            "from": "support",
                            "text": "Проблема подтверждена, работаем над исправлением",
                            "timestamp": "2024-11-25T14:30:00"
                        },
                        {
                            "from": "support",
                            "text": "Проблема устранена. Попробуйте сейчас.",
                            "timestamp": "2024-11-26T10:00:00"
                        },
                        {
                            "from": "user",
                            "text": "Спасибо, теперь все работает!",
                            "timestamp": "2024-11-26T10:30:00"
                        }
                    ]
                }
            ]

            # Сохраняем тестовые данные
            self.save_crm_data()

    def save_crm_data(self):
        """Сохраняет данные CRM в файл"""
        with open(self.crm_data_path, 'w', encoding='utf-8') as f:
            json.dump({
                'users': self.users,
                'tickets': self.tickets
            }, f, ensure_ascii=False, indent=2)

    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Находит пользователя по email"""
        for user in self.users:
            if user['email'].lower() == email.lower():
                return user
        return None

    def get_user_tickets(self, user_id: str, status: str = "all") -> List[Dict[str, Any]]:
        """Получает тикеты пользователя"""
        user_tickets = [t for t in self.tickets if t['user_id'] == user_id]

        if status != "all":
            user_tickets = [t for t in user_tickets if t['status'] == status]

        return user_tickets

    def get_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Получает тикет по ID"""
        for ticket in self.tickets:
            if ticket['ticket_id'] == ticket_id:
                return ticket
        return None

    def search_tickets(self, query: str, category: str = "all") -> List[Dict[str, Any]]:
        """Поиск тикетов по ключевым словам"""
        query_lower = query.lower()
        results = []

        for ticket in self.tickets:
            # Фильтр по категории
            if category != "all" and ticket['category'] != category:
                continue

            # Поиск в теме и описании
            if (query_lower in ticket['subject'].lower() or
                query_lower in ticket['description'].lower()):
                results.append(ticket)

        return results

    def get_user_subscription(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получает информацию о подписке"""
        for user in self.users:
            if user['user_id'] == user_id:
                return user.get('subscription')
        return None

    def create_ticket(self, user_id: str, category: str, subject: str,
                     description: str, priority: str = "medium") -> Dict[str, Any]:
        """Создает новый тикет"""
        # Генерируем ID
        ticket_count = len(self.tickets)
        ticket_id = f"TICK-{ticket_count + 1:03d}"

        now = datetime.now().isoformat()

        new_ticket = {
            "ticket_id": ticket_id,
            "user_id": user_id,
            "category": category,
            "subject": subject,
            "description": description,
            "status": "open",
            "priority": priority,
            "created_at": now,
            "updated_at": now,
            "assigned_to": None,
            "messages": [
                {
                    "from": "user",
                    "text": description,
                    "timestamp": now
                }
            ]
        }

        self.tickets.append(new_ticket)
        self.save_crm_data()

        return new_ticket

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Обрабатывает MCP запрос"""
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            return {
                "protocolVersion": "0.1.0",
                "serverInfo": {
                    "name": "crm-mcp-server",
                    "version": "1.0.0"
                },
                "capabilities": {
                    "tools": {}
                }
            }

        elif method == "tools/list":
            return {
                "tools": list(self.tools.values())
            }

        elif method == "tools/call":
            tool_name = params.get("name")
            arguments = params.get("arguments", {})

            if tool_name == "get_user_by_email":
                email = arguments.get("email")
                user = self.get_user_by_email(email)

                if user:
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(user, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                else:
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({"error": "User not found"}, ensure_ascii=False)
                            }
                        ]
                    }

            elif tool_name == "get_user_tickets":
                user_id = arguments.get("user_id")
                status = arguments.get("status", "all")
                tickets = self.get_user_tickets(user_id, status)

                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({"tickets": tickets, "count": len(tickets)}, ensure_ascii=False, indent=2)
                        }
                    ]
                }

            elif tool_name == "get_ticket":
                ticket_id = arguments.get("ticket_id")
                ticket = self.get_ticket(ticket_id)

                if ticket:
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(ticket, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                else:
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({"error": "Ticket not found"}, ensure_ascii=False)
                            }
                        ]
                    }

            elif tool_name == "search_tickets":
                query = arguments.get("query")
                category = arguments.get("category", "all")
                tickets = self.search_tickets(query, category)

                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps({"tickets": tickets, "count": len(tickets)}, ensure_ascii=False, indent=2)
                        }
                    ]
                }

            elif tool_name == "get_user_subscription":
                user_id = arguments.get("user_id")
                subscription = self.get_user_subscription(user_id)

                if subscription:
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps(subscription, ensure_ascii=False, indent=2)
                            }
                        ]
                    }
                else:
                    return {
                        "content": [
                            {
                                "type": "text",
                                "text": json.dumps({"error": "Subscription not found"}, ensure_ascii=False)
                            }
                        ]
                    }

            elif tool_name == "create_ticket":
                user_id = arguments.get("user_id")
                category = arguments.get("category")
                subject = arguments.get("subject")
                description = arguments.get("description")
                priority = arguments.get("priority", "medium")

                ticket = self.create_ticket(user_id, category, subject, description, priority)

                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(ticket, ensure_ascii=False, indent=2)
                        }
                    ]
                }

            return {"error": "Unknown tool"}

        return {"error": "Unknown method"}

    def run(self):
        """Запускает MCP сервер"""
        print("MCP CRM Server started", file=sys.stderr)

        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue

            try:
                request = json.loads(line)
                response = self.handle_request(request)

                output = json.dumps({
                    "jsonrpc": "2.0",
                    "id": request.get("id"),
                    "result": response
                })

                print(output)
                sys.stdout.flush()

            except Exception as e:
                error_response = json.dumps({
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": str(e)
                    }
                })
                print(error_response)
                sys.stdout.flush()


def main():
    """Главная функция"""
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Тестовый режим
        server = CRMMCPServer()

        print("=== Тест MCP CRM Server ===\n")

        print("1. Поиск пользователя по email:")
        user = server.get_user_by_email("ivan.petrov@example.com")
        if user:
            print(f"   ✓ Найден: {user['name']} (ID: {user['user_id']})")
            # Обработка разных форматов подписки
            sub = user.get('subscription', 'N/A')
            if isinstance(sub, dict):
                print(f"   Подписка: {sub.get('plan', 'N/A')}")
            else:
                print(f"   Подписка: {sub}")

        print("\n2. Получение тикетов пользователя:")
        tickets = server.get_user_tickets("user_001")
        print(f"   Найдено тикетов: {len(tickets)}")
        for t in tickets:
            print(f"   - {t['ticket_id']}: {t['subject']} [{t['status']}]")

        print("\n3. Поиск тикетов по ключевому слову 'авторизация':")
        results = server.search_tickets("авторизация")
        print(f"   Найдено: {len(results)} тикетов")
        for t in results:
            print(f"   - {t['ticket_id']}: {t['subject']}")

        print("\n4. Детали тикета TICK-001:")
        ticket = server.get_ticket("TICK-001")
        if ticket:
            print(f"   Тема: {ticket['subject']}")
            print(f"   Статус: {ticket['status']}")
            print(f"   Приоритет: {ticket['priority']}")
            if 'messages' in ticket:
                print(f"   Сообщений: {len(ticket['messages'])}")
            if 'context' in ticket:
                print(f"   Контекст: {ticket['context']}")

    else:
        # Запуск MCP сервера
        server = CRMMCPServer()
        server.run()


if __name__ == "__main__":
    main()
