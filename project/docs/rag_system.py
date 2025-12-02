#!/usr/bin/env python3
"""
RAG система для документации проекта Movike
Индексирует README.md и файлы из project/docs/ в векторную базу данных
"""

import os
import json
import sqlite3
from pathlib import Path
from typing import List, Dict, Tuple
import sys

# Простая RAG система без внешних зависимостей
# Использует TF-IDF для векторизации (можно заменить на эмбеддинги позже)

class SimpleRAG:
    """Простая RAG система на основе TF-IDF"""

    def __init__(self, db_path: str = "project/docs/rag_database.db"):
        self.db_path = db_path
        self.project_root = Path(__file__).parent.parent.parent
        self.init_database()

    def init_database(self):
        """Инициализация SQLite базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Таблица для хранения документов и их чанков
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT NOT NULL,
                chunk_index INTEGER NOT NULL,
                content TEXT NOT NULL,
                char_start INTEGER,
                char_end INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Таблица для метаданных
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS metadata (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        conn.commit()
        conn.close()
        print(f"✓ База данных инициализирована: {self.db_path}")

    def clear_database(self):
        """Очистка базы данных"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM documents')
        conn.commit()
        conn.close()
        print("✓ База данных очищена")

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[Tuple[str, int, int]]:
        """
        Разбивает текст на чанки с перекрытием

        Args:
            text: Исходный текст
            chunk_size: Размер чанка в символах
            overlap: Размер перекрытия между чанками

        Returns:
            List[(chunk_text, start_pos, end_pos)]
        """
        chunks = []
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))

            # Пытаемся найти конец предложения или параграфа
            if end < len(text):
                # Ищем конец предложения
                for sep in ['\n\n', '\n', '. ', '! ', '? ']:
                    last_sep = text[start:end].rfind(sep)
                    if last_sep != -1:
                        end = start + last_sep + len(sep)
                        break

            chunk = text[start:end].strip()
            if chunk:
                chunks.append((chunk, start, end))

            start = end - overlap if end < len(text) else end

        return chunks

    def index_file(self, file_path: str):
        """Индексирует один файл"""
        path = Path(file_path)

        if not path.exists():
            print(f"✗ Файл не найден: {file_path}")
            return

        # Читаем содержимое
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Разбиваем на чанки
        chunks = self.chunk_text(content)

        # Сохраняем в базу данных
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        relative_path = str(path.relative_to(self.project_root))

        for idx, (chunk, start, end) in enumerate(chunks):
            cursor.execute('''
                INSERT INTO documents (file_path, chunk_index, content, char_start, char_end)
                VALUES (?, ?, ?, ?, ?)
            ''', (relative_path, idx, chunk, start, end))

        conn.commit()
        conn.close()

        print(f"✓ Проиндексирован: {relative_path} ({len(chunks)} чанков)")

    def index_documentation(self):
        """Индексирует README.md и все файлы из project/docs/"""
        print("\n=== Индексация документации ===\n")

        # Очищаем базу
        self.clear_database()

        # Список файлов для индексации
        files_to_index = []

        # 1. README.md
        readme_path = self.project_root / "README.md"
        if readme_path.exists():
            files_to_index.append(readme_path)

        # 2. Все .md файлы из project/docs/
        docs_dir = self.project_root / "project" / "docs"
        if docs_dir.exists():
            for md_file in docs_dir.glob("*.md"):
                files_to_index.append(md_file)

        # Индексируем все файлы
        print(f"Найдено файлов для индексации: {len(files_to_index)}\n")

        for file_path in files_to_index:
            self.index_file(str(file_path))

        # Сохраняем метаданные
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO metadata (key, value)
            VALUES ('indexed_files_count', ?)
        ''', (len(files_to_index),))
        cursor.execute('''
            INSERT OR REPLACE INTO metadata (key, value)
            VALUES ('last_indexed', datetime('now'))
        ''')
        conn.commit()
        conn.close()

        print(f"\n✓ Индексация завершена: {len(files_to_index)} файлов")

    def search(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Простой поиск по содержимому (без векторов)
        В продакшене заменить на векторный поиск с эмбеддингами
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Простой полнотекстовый поиск
        # TODO: Заменить на векторный поиск с cosine similarity
        query_words = query.lower().split()

        cursor.execute('''
            SELECT file_path, chunk_index, content, char_start, char_end
            FROM documents
        ''')

        results = []
        for row in cursor.fetchall():
            file_path, chunk_idx, content, start, end = row
            content_lower = content.lower()

            # Подсчет совпадений слов
            score = sum(1 for word in query_words if word in content_lower)

            if score > 0:
                results.append({
                    'file_path': file_path,
                    'chunk_index': chunk_idx,
                    'content': content,
                    'char_start': start,
                    'char_end': end,
                    'score': score
                })

        # Сортируем по score
        results.sort(key=lambda x: x['score'], reverse=True)

        conn.close()

        return results[:limit]

    def get_stats(self) -> Dict:
        """Получить статистику по индексированным документам"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Общее количество чанков
        cursor.execute('SELECT COUNT(*) FROM documents')
        total_chunks = cursor.fetchone()[0]

        # Количество уникальных файлов
        cursor.execute('SELECT COUNT(DISTINCT file_path) FROM documents')
        total_files = cursor.fetchone()[0]

        # Метаданные
        cursor.execute('SELECT key, value FROM metadata')
        metadata = dict(cursor.fetchall())

        conn.close()

        return {
            'total_chunks': total_chunks,
            'total_files': total_files,
            'metadata': metadata
        }


def main():
    """Главная функция"""
    rag = SimpleRAG()

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "index":
            # Индексация документации
            rag.index_documentation()

        elif command == "search":
            # Поиск
            if len(sys.argv) < 3:
                print("Использование: python3 rag_system.py search 'ваш запрос'")
                return

            query = ' '.join(sys.argv[2:])
            print(f"\nПоиск: '{query}'\n")

            results = rag.search(query, limit=5)

            if not results:
                print("Ничего не найдено")
                return

            print(f"Найдено результатов: {len(results)}\n")

            for idx, result in enumerate(results, 1):
                print(f"{idx}. {result['file_path']} (chunk {result['chunk_index']}, score: {result['score']})")
                print(f"   {result['content'][:200]}...")
                print()

        elif command == "stats":
            # Статистика
            stats = rag.get_stats()
            print("\n=== Статистика RAG системы ===\n")
            print(f"Всего файлов: {stats['total_files']}")
            print(f"Всего чанков: {stats['total_chunks']}")
            print(f"\nМетаданные:")
            for key, value in stats['metadata'].items():
                print(f"  {key}: {value}")

        else:
            print(f"Неизвестная команда: {command}")
            print("\nДоступные команды:")
            print("  index  - индексировать документацию")
            print("  search - поиск по документации")
            print("  stats  - статистика")

    else:
        print("RAG система для документации Movike")
        print("\nИспользование:")
        print("  python3 rag_system.py index           # Индексация")
        print("  python3 rag_system.py search 'запрос' # Поиск")
        print("  python3 rag_system.py stats           # Статистика")


if __name__ == "__main__":
    main()
