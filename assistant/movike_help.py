#!/usr/bin/env python3
"""
Movike Assistant - Полностью автономный help скрипт
Использование: python3 movike_help.py "ваш вопрос"
"""

import sys
import json
import re
from pathlib import Path

# ============= КОНФИГУРАЦИЯ =============

SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
if PROJECT_ROOT.name == "project":
    PROJECT_ROOT = PROJECT_ROOT.parent

README_PATH = PROJECT_ROOT / "README.md"
DOCS_DIR = SCRIPT_DIR.parent
APP_SRC = PROJECT_ROOT / "app" / "src" / "main" / "java"
INDEX_PATH = SCRIPT_DIR / "rag_index.json"

# ============= ИНДЕКСАЦИЯ =============

def chunk_text(text, chunk_size=500):
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

def index_documentation():
    """Индексирует документацию"""
    documents = []

    # README
    if README_PATH.exists():
        with open(README_PATH, 'r', encoding='utf-8') as f:
            content = f.read()
        for idx, chunk in enumerate(chunk_text(content)):
            documents.append({
                'file': 'README.md',
                'chunk_index': idx,
                'content': chunk
            })

    # MD файлы из docs
    for md_file in sorted(DOCS_DIR.glob("*.md")):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        for idx, chunk in enumerate(chunk_text(content)):
            documents.append({
                'file': f"project/docs/{md_file.name}",
                'chunk_index': idx,
                'content': chunk
            })

    return documents

def index_classes():
    """Индексирует классы Kotlin"""
    documents = []

    if not APP_SRC.exists():
        return documents

    for kt_file in APP_SRC.rglob("*.kt"):
        try:
            with open(kt_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            continue

        lines = content.split('\n')
        patterns = [r'(class|interface|object|data class|sealed class|enum class)\s+(\w+)']

        for i, line in enumerate(lines):
            for pattern in patterns:
                match = re.search(pattern, line.strip())
                if match and not line.strip().startswith('//'):
                    class_type = match.group(1)
                    class_name = match.group(2)

                    # Код класса
                    class_code = []
                    for j in range(i, min(i + 30, len(lines))):
                        class_code.append(lines[j])
                        if '}' in lines[j] and j > i:
                            break

                    code_str = '\n'.join(class_code)
                    relative_path = str(kt_file.relative_to(PROJECT_ROOT))

                    formatted = f"# {class_type} {class_name}\n\n"
                    formatted += f"**Файл:** {relative_path}:{i+1}\n\n"
                    formatted += f"**Код:**\n```kotlin\n{code_str}\n```\n"

                    documents.append({
                        'file': f"{relative_path}:{i+1}",
                        'chunk_index': 0,
                        'content': formatted
                    })
                    break

    return documents

def create_index():
    """Создаёт индекс"""
    print("🔄 Создание индекса...\n")

    docs = index_documentation()
    print(f"✓ Документация: {len(docs)} чанков")

    classes = index_classes()
    print(f"✓ Классы: {len(classes)} классов")

    all_docs = docs + classes

    with open(INDEX_PATH, 'w', encoding='utf-8') as f:
        json.dump({
            'total_documents': len(all_docs),
            'documents': all_docs
        }, f, ensure_ascii=False, indent=2)

    print(f"\n✅ Всего: {len(all_docs)} документов")
    print(f"✅ Индекс: {INDEX_PATH}\n")

    return len(all_docs)

# ============= ПОИСК =============

def search(query, limit=3):
    """Поиск в RAG"""
    if not INDEX_PATH.exists():
        print("❌ Индекс не найден. Создаю...\n")
        create_index()

    with open(INDEX_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    documents = data.get('documents', [])

    if not documents:
        print("❌ Индекс пустой. Пересоздаю...\n")
        create_index()
        with open(INDEX_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        documents = data.get('documents', [])

    query_words = set(query.lower().split())
    results = []

    for doc in documents:
        content_lower = doc['content'].lower()
        matches = sum(1 for word in query_words if word in content_lower)

        if matches > 0:
            results.append({**doc, 'score': matches})

    results.sort(key=lambda x: x['score'], reverse=True)
    return results[:limit]

# ============= MAIN =============

def main():
    if len(sys.argv) < 2:
        print("Movike Assistant")
        print("\nИспользование:")
        print("  python3 movike_help.py 'ваш вопрос'")
        print("  python3 movike_help.py index  # Переиндексация")
        print("\nПримеры:")
        print("  python3 movike_help.py 'ApiService'")
        print("  python3 movike_help.py 'структура проекта'")
        return

    if sys.argv[1] == "index":
        create_index()
        return

    query = ' '.join(sys.argv[1:])

    print("=" * 60)
    print(f"  Movike Assistant - Вопрос: {query}")
    print("=" * 60)
    print()

    results = search(query, limit=3)

    if not results:
        print("❌ Ничего не найдено\n")
        return

    print(f"✅ Найдено: {len(results)} результатов\n")
    print("-" * 60)

    for i, result in enumerate(results, 1):
        print(f"\n📄 Результат #{i}")
        print(f"   Файл: {result['file']}")
        print(f"   Релевантность: {result['score']}")
        print(f"\n   Содержимое:")
        print("   " + "-" * 56)

        for line in result['content'].split('\n')[:25]:
            print(f"   {line}")

        print("   " + "-" * 56)

    print(f"\n{'=' * 60}\n")

if __name__ == "__main__":
    main()
