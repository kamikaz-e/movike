#!/usr/bin/env python3
"""Тест RAG системы"""

import sys
from pathlib import Path

# Добавляем путь к модулям
sys.path.insert(0, str(Path(__file__).parent))

from simple_rag import SimpleRAG

print("=== Тест RAG системы ===\n")

rag = SimpleRAG()

# Попытка загрузить индекс
if rag.load_index():
    print(f"✓ Индекс загружен: {len(rag.documents)} документов\n")

    # Тест поиска
    query = "ApiService"
    print(f"Поиск: '{query}'\n")

    results = rag.search(query, limit=3)

    if results:
        print(f"Найдено: {len(results)} результатов\n")
        for i, r in enumerate(results, 1):
            print(f"{i}. {r['file']} (score: {r['score']})")
            preview = r['content'][:200].replace('\n', ' ')
            print(f"   {preview}...\n")
    else:
        print("Ничего не найдено")
else:
    print("❌ Индекс не загружен")
    print(f"Ожидаемый путь: {rag.index_path}")
