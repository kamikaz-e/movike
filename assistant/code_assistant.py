#!/usr/bin/env python3
"""
Code Assistant - консольный помощник для вопросов о коде
Использует RAG для поиска в документации и коде проекта Movike

Использование:
    python3 code_assistant.py                    # Интерактивный режим
    python3 code_assistant.py "вопрос о коде"    # Один вопрос
    python3 code_assistant.py index              # Индексация документации
"""

import sys
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from simple_rag import SimpleRAG
from mcp_git_server import GitMCPServer


class CodeAssistant:
    """Ассистент для ответов на вопросы о коде проекта"""

    def __init__(self):
        self.assistant_dir = Path(__file__).parent
        self.project_root = self.assistant_dir.parent
        
        # Инициализация RAG системы
        self.rag = SimpleRAG()
        
        # Инициализация MCP Git сервера для контекста
        self.git_server = GitMCPServer()
        
        # Загружаем RAG индекс если есть
        if self.rag.index_path.exists():
            self.rag.load_index()

        print("✓ Code Assistant инициализирован", file=sys.stderr)
        if self.rag.documents:
            print(f"✓ Загружено документов в RAG: {len(self.rag.documents)}", file=sys.stderr)

    def search_documentation(self, query: str, limit: int = 3) -> List[Dict[str, Any]]:
        """Поиск в документации через RAG"""
        if not self.rag.documents:
            return []
        return self.rag.search(query, limit=limit)

    def search_code_files(self, query: str) -> List[Dict[str, Any]]:
        """Поиск в Kotlin файлах проекта"""
        results = []
        query_lower = query.lower()
        
        # Ищем все .kt файлы в проекте
        for kt_file in self.project_root.rglob('*.kt'):
            # Пропускаем build директории
            relative_path = kt_file.relative_to(self.project_root)
            path_str = str(relative_path)
            
            if any(excluded in path_str for excluded in ['/build/', '/.gradle/', '/.idea/']):
                continue
            
            try:
                with open(kt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Простой поиск по ключевым словам
                lines = content.split('\n')
                matching_lines = []
                
                for i, line in enumerate(lines, 1):
                    if query_lower in line.lower():
                        # Контекст: 2 строки до и после
                        start = max(0, i - 3)
                        end = min(len(lines), i + 3)
                        context = '\n'.join(lines[start:end])
                        
                        matching_lines.append({
                            'line_number': i,
                            'line': line.strip(),
                            'context': context
                        })
                
                if matching_lines:
                    results.append({
                        'file': path_str,
                        'matches': matching_lines[:5]  # Максимум 5 совпадений на файл
                    })
            except Exception as e:
                continue
        
        return results[:10]  # Максимум 10 файлов

    def get_file_content(self, file_path: str) -> Optional[str]:
        """Получает содержимое файла"""
        full_path = self.project_root / file_path
        
        if not full_path.exists():
            return None
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return None

    def get_git_context(self) -> Dict[str, Any]:
        """Получает контекст из git (ветка, изменения)"""
        try:
            branch = self.git_server.get_current_branch()
            branch_info = self.git_server.get_branch_info()
            
            return {
                'current_branch': branch,
                'status': branch_info.get('status', ''),
                'last_commit': branch_info.get('last_commit', '')
            }
        except:
            return {}

    def answer_question(self, question: str, include_code: bool = True) -> Dict[str, Any]:
        """
        Главный метод для ответа на вопросы о коде
        Комбинирует RAG (документация) и поиск в коде
        """
        response = {
            "question": question,
            "answer": "",
            "sources": {
                "documentation": [],
                "code_files": [],
                "git_context": {}
            },
            "confidence": "medium"
        }

        # 1. Поиск в документации через RAG
        doc_results = self.search_documentation(question, limit=5)
        response["sources"]["documentation"] = doc_results

        # 2. Поиск в коде (если включен)
        if include_code:
            code_results = self.search_code_files(question)
            response["sources"]["code_files"] = code_results

        # 3. Контекст из git
        git_context = self.get_git_context()
        response["sources"]["git_context"] = git_context

        # 4. Формируем ответ
        response["answer"] = self.generate_answer(question, response["sources"])

        # 5. Определяем уверенность ответа
        if doc_results and len(doc_results) > 0:
            response["confidence"] = "high"
        elif response["sources"]["code_files"]:
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

        # Найденные файлы кода
        if sources["code_files"]:
            answer_parts.append(f"\n💻 НАЙДЕННЫЕ ФАЙЛЫ КОДА ({len(sources['code_files'])}):\n")
            for code_file in sources["code_files"][:5]:
                answer_parts.append(f"📁 {code_file['file']}")
                
                for match in code_file['matches'][:2]:  # Показываем 2 первых совпадения
                    answer_parts.append(f"   Строка {match['line_number']}: {match['line'][:80]}")
                
                if len(code_file['matches']) > 2:
                    answer_parts.append(f"   ... и ещё {len(code_file['matches']) - 2} совпадений")
                answer_parts.append("")

        # Git контекст
        git_ctx = sources.get("git_context", {})
        if git_ctx.get('current_branch'):
            answer_parts.append(f"\n🌿 GIT КОНТЕКСТ:")
            answer_parts.append(f"   Ветка: {git_ctx.get('current_branch')}")
            if git_ctx.get('last_commit'):
                answer_parts.append(f"   Последний коммит: {git_ctx.get('last_commit')}")
            answer_parts.append("")

        # Если ничего не найдено
        if not answer_parts:
            answer_parts.append("❌ К сожалению, не удалось найти информацию по вашему вопросу.")
            answer_parts.append("\n💡 Рекомендации:")
            answer_parts.append("• Переиндексируйте документацию: python3 code_assistant.py index")
            answer_parts.append("• Попробуйте другие ключевые слова")
            answer_parts.append("• Проверьте наличие файлов README.md и project/docs/*.md")

        return "\n".join(answer_parts)

    def interactive_mode(self):
        """Интерактивный режим работы с ассистентом"""
        print("\n" + "="*60)
        print("💻 MOVIKE CODE ASSISTANT")
        print("="*60)
        print("\nДобро пожаловать! Я помогу вам с вопросами о коде проекта Movike.")
        print("\nКоманды:")
        print("  • Введите ваш вопрос о коде")
        print("  • 'index' - переиндексировать документацию")
        print("  • 'file:<путь>' - показать содержимое файла")
        print("  • 'code' - включить/выключить поиск в коде")
        print("  • 'exit' - выход")
        print("="*60 + "\n")

        include_code = True

        while True:
            try:
                user_input = input("❓ Вопрос: ").strip()

                if not user_input:
                    continue

                if user_input.lower() == 'exit':
                    print("\n👋 До свидания! Удачного кодинга!")
                    break

                # Команда: индексация
                if user_input.lower() == 'index':
                    print("\n📚 Индексация документации...\n")
                    self.rag.index_all()
                    self.rag.load_index()
                    print("\n✅ Индексация завершена!\n")
                    continue

                # Команда: показать файл
                if user_input.lower().startswith('file:'):
                    file_path = user_input[5:].strip()
                    content = self.get_file_content(file_path)
                    if content:
                        print(f"\n📄 {file_path}:\n")
                        print("-" * 60)
                        # Показываем первые 50 строк
                        lines = content.split('\n')
                        for i, line in enumerate(lines[:50], 1):
                            print(f"{i:4d} | {line}")
                        if len(lines) > 50:
                            print(f"\n... и ещё {len(lines) - 50} строк")
                        print("-" * 60 + "\n")
                    else:
                        print(f"\n❌ Файл '{file_path}' не найден\n")
                    continue

                # Команда: переключить поиск в коде
                if user_input.lower() == 'code':
                    include_code = not include_code
                    status = "включен" if include_code else "выключен"
                    print(f"\n💻 Поиск в коде: {status}\n")
                    continue

                # Обычный вопрос
                print("\n🔍 Ищу информацию...\n")

                result = self.answer_question(user_input, include_code=include_code)

                print("="*60)
                print(result['answer'])
                print("="*60)
                print(f"\n💡 Уверенность: {result['confidence']}")
                
                # Предлагаем показать полный файл если нашли совпадения
                if result['sources']['code_files']:
                    first_file = result['sources']['code_files'][0]['file']
                    print(f"\n💡 Показать файл? Введите: file:{first_file}")
                print()

            except KeyboardInterrupt:
                print("\n\n👋 До свидания!")
                break
            except Exception as e:
                print(f"\n❌ Ошибка: {e}\n")

    def cli_mode(self, question: str, include_code: bool = True):
        """Режим командной строки для одного вопроса"""
        result = self.answer_question(question, include_code=include_code)

        print("\n" + "="*60)
        print("💻 MOVIKE CODE ASSISTANT")
        print("="*60)
        print(f"\n❓ Вопрос: {question}")
        print("\n" + "-"*60)
        print(result['answer'])
        print("-"*60)
        print(f"\n💡 Уверенность ответа: {result['confidence']}")
        print()


def main():
    """Главная функция"""
    assistant = CodeAssistant()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "index":
            # Индексация документации
            print("📚 Индексация документации...\n")
            assistant.rag.index_all()
            assistant.rag.load_index()
            print("\n✅ Индексация завершена!")

        elif command == "help" or command == "--help" or command == "-h":
            print(__doc__)
            print("\nПримеры:")
            print('  python3 code_assistant.py "Как использовать ApiService?"')
            print('  python3 code_assistant.py "Где находится FeedViewModel?"')
            print('  python3 code_assistant.py "Как работает авторизация?"')

        else:
            # Один вопрос из командной строки
            question = command
            include_code = True
            
            # Проверяем флаги
            if len(sys.argv) > 2:
                for arg in sys.argv[2:]:
                    if arg == '--no-code':
                        include_code = False
            
            assistant.cli_mode(question, include_code=include_code)

    else:
        # Интерактивный режим по умолчанию
        assistant.interactive_mode()


if __name__ == "__main__":
    main()

