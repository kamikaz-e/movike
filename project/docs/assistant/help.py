#!/usr/bin/env python3
"""
Простой help скрипт для Movike Assistant
Использование: python3 help.py "ваш вопрос"
"""

import sys
import json
from pathlib import Path

# Путь к индексу
INDEX_FILE = Path(__file__).parent / "rag_index.json"

def search_rag(query, limit=3):
    """Простой поиск в RAG"""
    if not INDEX_FILE.exists():
        print(f"❌ Файл не найден: {INDEX_FILE}")
        print("\n💡 Запустите: python3 quick_index.py")
        return []

    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    documents = data.get('documents', [])

    if not documents:
        print(f"❌ Индекс пустой (0 документов)")
        return []

    query_words = set(query.lower().split())
    results = []

    for doc in documents:
        content_lower = doc['content'].lower()
        matches = sum(1 for word in query_words if word in content_lower)

        if matches > 0:
            results.append({
                **doc,
                'score': matches
            })

    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]

def main():
    if len(sys.argv) < 2:
        print("Использование: python3 help.py 'ваш вопрос'")
        print("\nПримеры:")
        print("  python3 help.py 'ApiService'")
        print("  python3 help.py 'структура проекта'")
        print("  python3 help.py 'FeedViewModel'")
        return

    query = ' '.join(sys.argv[1:])

    print("=" * 60)
    print(f"  Movike Assistant - Вопрос: {query}")
    print("=" * 60)
    print()

    results = search_rag(query, limit=3)

    if not results:
        print("❌ Ничего не найдено")
        print("\n💡 Попробуйте:")
        print("  - Другие ключевые слова")
        print("  - Переиндексацию: python3 quick_index.py")
        return

    print(f"✅ Найдено: {len(results)} результатов\n")
    print("-" * 60)

    for i, result in enumerate(results, 1):
        print(f"\n📄 Результат #{i}")
        print(f"   Файл: {result['file']}")
        print(f"   Релевантность: {result['score']}")
        print(f"\n   Содержимое:")
        print("   " + "-" * 56)

        content = result['content']
        lines = content.split('\n')
        for line in lines[:25]:
            print(f"   {line}")

        if len(lines) > 25:
            print(f"   ... ({len(lines) - 25} строк скрыто)")

        print("   " + "-" * 56)

    print(f"\n{'=' * 60}\n")

if __name__ == "__main__":
    main()
