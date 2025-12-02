#!/usr/bin/env python3
"""
Movike Project Assistant
Единая точка входа для всех AI-ассистент функций проекта

Использование:
    python3 assistant.py help "ваш вопрос"
    python3 assistant.py search "ключевые слова"
    python3 assistant.py git
    python3 assistant.py stats
    python3 assistant.py reindex
"""

import sys
import os
from pathlib import Path

# Добавляем текущую директорию в путь для импорта
ASSISTANT_DIR = Path(__file__).parent
sys.path.insert(0, str(ASSISTANT_DIR))

# Импортируем модули
from simple_rag import SimpleRAG
from index_classes import KotlinClassExtractor, merge_with_existing_rag
import subprocess
import json


class MovikAssistant:
    """Главный класс ассистента проекта Movike"""

    def __init__(self):
        self.assistant_dir = ASSISTANT_DIR
        # assistant/ находится в корне проекта, поэтому parent - это корень
        self.project_root = self.assistant_dir.parent
        self.rag = SimpleRAG()

    def _read_documentation_fallback(self, question: str):
        """Fallback: читает документацию напрямую, если RAG пустой"""
        print("📚 RAG индекс пустой. Читаю документацию напрямую...\n")
        
        results = []
        query_words = set(question.lower().split())
        
        # Читаем README.md
        readme_path = self.project_root / "README.md"
        if readme_path.exists():
            try:
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    content_lower = content.lower()
                    matches = sum(1 for word in query_words if word in content_lower)
                    if matches > 0:
                        results.append({
                            'file': 'README.md',
                            'score': matches,
                            'content': content
                        })
            except Exception as e:
                print(f"⚠️  Ошибка чтения README.md: {e}\n")
        
        # Читаем файлы из project/docs/
        docs_dir = self.project_root / "project" / "docs"
        if docs_dir.exists():
            for md_file in sorted(docs_dir.glob("*.md")):
                try:
                    with open(md_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        content_lower = content.lower()
                        matches = sum(1 for word in query_words if word in content_lower)
                        if matches > 0:
                            relative_path = str(md_file.relative_to(self.project_root))
                            results.append({
                                'file': relative_path,
                                'score': matches,
                                'content': content
                            })
                except Exception as e:
                    print(f"⚠️  Ошибка чтения {md_file.name}: {e}\n")
        
        # Сортируем по релевантности
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:3]

    def help_command(self, question: str):
        """Обрабатывает команду /help"""
        print(f"\n{'='*60}")
        print(f"  Movike Assistant - Вопрос: {question}")
        print(f"{'='*60}\n")

        # Шаг 1: Проверяем, есть ли индекс
        index_exists = self.rag.index_path.exists()
        index_loaded = False
        
        if index_exists:
            index_loaded = self.rag.load_index()
            if index_loaded and len(self.rag.documents) == 0:
                index_loaded = False
        
        # Шаг 2: Поиск в RAG или fallback
        if index_loaded and len(self.rag.documents) > 0:
            print("🔍 Поиск в RAG базе данных...\n")
            results = self.rag.search(question, limit=3)
        else:
            if not index_exists:
                print("⚠️  RAG индекс не найден. Использую прямое чтение документации...\n")
            else:
                print("⚠️  RAG индекс пустой. Использую прямое чтение документации...\n")
            results = self._read_documentation_fallback(question)

        if not results:
            print("❌ Ничего не найдено в документации")
            print("\n💡 Попробуйте:")
            print("   - Переиндексировать: python3 assistant.py reindex")
            print("   - Использовать другие ключевые слова")
            print("   - Проверить наличие файлов README.md и project/docs/*.md")
            return

        print(f"✅ Найдено результатов: {len(results)}\n")
        print("-" * 60)

        # Выводим результаты
        for idx, result in enumerate(results, 1):
            print(f"\n📄 Результат #{idx}")
            print(f"   Файл: {result['file']}")
            print(f"   Релевантность: {result['score']}")
            print(f"\n   Содержимое:")
            print("   " + "-" * 56)

            # Форматируем вывод
            content = result['content']
            lines = content.split('\n')
            for line in lines[:20]:  # Первые 20 строк
                print(f"   {line}")

            if len(lines) > 20:
                print(f"   ... ({len(lines) - 20} строк скрыто)")

            print("   " + "-" * 56)

        print(f"\n{'='*60}\n")
        
        # Предлагаем переиндексацию, если индекс пустой
        if not index_loaded or len(self.rag.documents) == 0:
            print("💡 Совет: Для более быстрого поиска запустите переиндексацию:")
            print("   python3 assistant.py reindex\n")

    def search_command(self, query: str):
        """Прямой поиск в RAG"""
        print(f"\n🔍 Поиск: '{query}'\n")
        
        # Проверяем, есть ли индекс
        index_exists = self.rag.index_path.exists()
        index_loaded = False
        
        if index_exists:
            index_loaded = self.rag.load_index()
            if index_loaded and len(self.rag.documents) == 0:
                index_loaded = False
        
        # Поиск в RAG или fallback
        if index_loaded and len(self.rag.documents) > 0:
            results = self.rag.search(query, limit=5)
        else:
            if not index_exists:
                print("⚠️  RAG индекс не найден. Использую прямое чтение документации...\n")
            else:
                print("⚠️  RAG индекс пустой. Использую прямое чтение документации...\n")
            results = self._read_documentation_fallback(query)

        if not results:
            print("❌ Ничего не найдено")
            print("\n💡 Попробуйте:")
            print("   - Переиндексировать: python3 assistant.py reindex")
            print("   - Использовать другие ключевые слова")
            return

        print(f"✅ Найдено: {len(results)} результатов\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['file']} (score: {r['score']})")
            preview = r['content'][:150].replace('\n', ' ')
            print(f"   {preview}...\n")
        
        # Предлагаем переиндексацию, если индекс пустой
        if not index_loaded or len(self.rag.documents) == 0:
            print("💡 Совет: Для более быстрого поиска запустите переиндексацию:")
            print("   python3 assistant.py reindex\n")

    def git_command(self):
        """Информация о git ветке через MCP"""
        print("\n📊 Git информация через MCP\n")

        mcp_script = self.assistant_dir / "mcp_git_server.py"

        try:
            result = subprocess.run(
                ['python3', str(mcp_script), 'test'],
                capture_output=True,
                text=True,
                timeout=5
            )
            print(result.stdout)
        except Exception as e:
            print(f"❌ Ошибка: {e}")

    def stats_command(self):
        """Статистика RAG системы"""
        print("\n📈 Статистика RAG системы\n")

        if not self.rag.load_index():
            print("❌ RAG индекс не найден. Запустите: python3 assistant.py reindex")
            return

        # Группировка по файлам
        files = {}
        for doc in self.rag.documents:
            file = doc['file']
            files[file] = files.get(file, 0) + 1

        print(f"Всего документов: {len(self.rag.documents)}\n")

        # Разделяем документацию и классы
        doc_files = {k: v for k, v in files.items() if not k.startswith('app/')}
        class_files = {k: v for k, v in files.items() if k.startswith('app/')}

        print("📚 Документация:")
        for f, count in sorted(doc_files.items()):
            print(f"  {f}: {count} чанков")

        print(f"\n💻 Классы проекта: {len(class_files)} файлов")
        print(f"\n✅ Всего в RAG: {len(self.rag.documents)} документов")

    def reindex_command(self):
        """Полная переиндексация"""
        print("\n🔄 Полная переиндексация...\n")

        # 1. Индексация документации
        print("📚 Шаг 1: Индексация документации")
        self.rag.index_all()

        # 2. Индексация классов
        print("\n💻 Шаг 2: Индексация классов")

        extractor = KotlinClassExtractor(self.project_root)
        extractor.scan_project()

        classes_output = self.assistant_dir / "classes_index.json"
        rag_index = self.assistant_dir / "rag_index.json"

        extractor.save_to_rag(classes_output)

        # 3. Объединение
        print("\n🔗 Шаг 3: Объединение индексов")
        merge_with_existing_rag(classes_output, rag_index)

        print("\n✅ Переиндексация завершена!")

    def interactive_mode(self):
        """Интерактивный режим"""
        print("\n" + "="*60)
        print("  🤖 Movike Project Assistant - Интерактивный режим")
        print("="*60)
        print("\nКоманды:")
        print("  help <вопрос>  - Задать вопрос о проекте")
        print("  search <текст> - Поиск в документации")
        print("  git            - Информация о git ветке")
        print("  stats          - Статистика RAG")
        print("  reindex        - Переиндексация")
        print("  exit           - Выход")
        print("\n" + "="*60 + "\n")

        while True:
            try:
                user_input = input("Assistant> ").strip()

                if not user_input:
                    continue

                if user_input.lower() == 'exit':
                    print("Выход...")
                    break

                parts = user_input.split(maxsplit=1)
                command = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                if command == 'help':
                    if not args:
                        print("Использование: help <ваш вопрос>")
                    else:
                        self.help_command(args)

                elif command == 'search':
                    if not args:
                        print("Использование: search <текст>")
                    else:
                        self.search_command(args)

                elif command == 'git':
                    self.git_command()

                elif command == 'stats':
                    self.stats_command()

                elif command == 'reindex':
                    self.reindex_command()

                else:
                    print(f"Неизвестная команда: {command}")
                    print("Доступные команды: help, search, git, stats, reindex, exit")

            except KeyboardInterrupt:
                print("\n\nВыход...")
                break
            except Exception as e:
                print(f"Ошибка: {e}")


def main():
    assistant = MovikAssistant()

    if len(sys.argv) == 1:
        # Интерактивный режим
        assistant.interactive_mode()
    else:
        command = sys.argv[1].lower()
        
        # Поддержка /help как синонима help
        if command == '/help' or command == 'help':
            command = 'help'

        if command == 'help':
            question = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ""
            if not question:
                print("Использование: python3 assistant.py help 'ваш вопрос'")
                return
            assistant.help_command(question)

        elif command == 'search':
            query = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ""
            if not query:
                print("Использование: python3 assistant.py search 'текст'")
                return
            assistant.search_command(query)

        elif command == 'git':
            assistant.git_command()

        elif command == 'stats':
            assistant.stats_command()

        elif command == 'reindex':
            assistant.reindex_command()

        elif command == 'interactive' or command == '-i':
            assistant.interactive_mode()

        else:
            print(f"Неизвестная команда: {command}")
            print("\nИспользование:")
            print("  python3 assistant.py help 'вопрос'       # Задать вопрос")
            print("  python3 assistant.py /help 'вопрос'      # То же самое (синоним)")
            print("  python3 assistant.py search 'текст'      # Поиск")
            print("  python3 assistant.py git                 # Git информация")
            print("  python3 assistant.py stats               # Статистика")
            print("  python3 assistant.py reindex             # Переиндексация")
            print("  python3 assistant.py interactive         # Интерактивный режим")
            print("  python3 assistant.py                     # Интерактивный режим (по умолчанию)")
            print("\n💡 Важно: В zsh используйте одинарные кавычки для вопросов со знаками препинания:")
            print("   python3 assistant.py help 'Какие модули есть в проекте?'")


if __name__ == "__main__":
    main()
