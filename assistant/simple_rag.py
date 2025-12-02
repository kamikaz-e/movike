#!/usr/bin/env python3
"""
Простая RAG система для документации Movike
Индексирует README.md и файлы из project/docs/
"""

import os
import json
from pathlib import Path
from typing import List, Dict

class SimpleRAG:
    """Простая RAG система без внешних зависимостей"""

    def __init__(self):
        self.assistant_dir = Path(__file__).parent
        # assistant/ находится в корне проекта, поэтому parent - это корень
        self.project_root = self.assistant_dir.parent
        self.index_path = self.assistant_dir / "rag_index.json"
        self.documents = []

    def chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Разбивает текст на чанки"""
        chunks = []
        lines = text.split('\n')
        current_chunk = []
        current_size = 0

        for line in lines:
            line_size = len(line)

            if current_size + line_size > chunk_size and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size

        if current_chunk:
            chunks.append('\n'.join(current_chunk))

        return chunks

    def index_file(self, file_path: Path) -> int:
        """Индексирует один файл"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        chunks = self.chunk_text(content)
        relative_path = str(file_path.relative_to(self.project_root))

        for idx, chunk in enumerate(chunks):
            self.documents.append({
                'file': relative_path,
                'chunk_index': idx,
                'content': chunk
            })

        return len(chunks)

    def index_all(self):
        """Индексирует README.md и project/docs/*.md"""
        print("=== Индексация документации ===\n")

        self.documents = []
        total_chunks = 0

        # 1. README.md
        readme = self.project_root / "README.md"
        if readme.exists():
            chunks = self.index_file(readme)
            print(f"✓ README.md: {chunks} чанков")
            total_chunks += chunks

        # 2. Файлы из project/docs/
        docs_dir = self.project_root / "project" / "docs"
        if docs_dir.exists():
            for md_file in sorted(docs_dir.glob("*.md")):
                chunks = self.index_file(md_file)
                print(f"✓ {md_file.name}: {chunks} чанков")
                total_chunks += chunks

        # Сохраняем индекс
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump({
                'total_documents': len(self.documents),
                'documents': self.documents
            }, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Всего проиндексировано: {total_chunks} чанков")
        print(f"✓ Индекс сохранён: {self.index_path}")

    def load_index(self):
        """Загружает индекс из файла"""
        if not self.index_path.exists():
            print("Индекс не найден. Запустите: python3 simple_rag.py index")
            return False

        with open(self.index_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.documents = data['documents']

        return True

    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """Улучшенный поиск по ключевым словам с учетом контекста"""
        if not self.documents:
            if not self.load_index():
                return []

        query_lower = query.lower()
        query_words = set(query_lower.split())
        results = []

        for doc in self.documents:
            content_lower = doc['content'].lower()
            file_lower = doc['file'].lower()

            # Базовый подсчёт совпадений
            matches = sum(1 for word in query_words if word in content_lower)
            
            if matches == 0:
                continue

            score = matches

            # Бонусы за релевантность:
            # 1. Если запрос содержит "модули" и в контенте есть заголовок "## Модули" или "### app", "### feature"
            if 'модули' in query_lower or 'модуль' in query_lower:
                if '## модули' in content_lower or '### app' in content_lower or '### feature' in content_lower or '### shared' in content_lower:
                    score += 10
            
            # 2. Если запрос содержит "структура" и в контенте есть "структура проекта"
            if 'структура' in query_lower:
                if 'структура проекта' in content_lower or '## структура' in content_lower:
                    score += 5
            
            # 3. Если запрос содержит "api" и в контенте есть "## api" или "api reference"
            if 'api' in query_lower:
                if '## api' in content_lower or 'api reference' in content_lower:
                    score += 5
            
            # 4. Бонус за точное совпадение фразы
            if query_lower in content_lower:
                score += 3
            
            # 5. Бонус за совпадение в начале контента (заголовки важнее)
            first_200 = content_lower[:200]
            if any(word in first_200 for word in query_words):
                score += 2

            results.append({
                **doc,
                'score': score
            })

        # Сортировка по релевантности
        results.sort(key=lambda x: x['score'], reverse=True)

        return results[:limit]


def main():
    import sys

    rag = SimpleRAG()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "index":
            rag.index_all()

        elif command == "search":
            query = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ""
            if not query:
                print("Использование: python3 simple_rag.py search 'запрос'")
                return

            print(f"\nПоиск: '{query}'\n")
            results = rag.search(query)

            if not results:
                print("Ничего не найдено")
                return

            print(f"Найдено: {len(results)} результатов\n")
            for i, r in enumerate(results, 1):
                print(f"{i}. {r['file']} (chunk {r['chunk_index']}, score: {r['score']})")
                preview = r['content'][:150].replace('\n', ' ')
                print(f"   {preview}...\n")

        elif command == "stats":
            if rag.load_index():
                print(f"\nВсего документов: {len(rag.documents)}")

                # Группировка по файлам
                files = {}
                for doc in rag.documents:
                    files[doc['file']] = files.get(doc['file'], 0) + 1

                print("\nФайлы:")
                for f, count in files.items():
                    print(f"  {f}: {count} чанков")

        else:
            print(f"Неизвестная команда: {command}")

    else:
        print("Простая RAG система для Movike")
        print("\nКоманды:")
        print("  python3 simple_rag.py index           # Индексация")
        print("  python3 simple_rag.py search 'запрос' # Поиск")
        print("  python3 simple_rag.py stats           # Статистика")


if __name__ == "__main__":
    main()
