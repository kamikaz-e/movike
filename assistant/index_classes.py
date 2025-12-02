#!/usr/bin/env python3
"""
Скрипт для индексации классов и интерфейсов проекта Movike в RAG
Извлекает информацию о классах из Kotlin файлов и добавляет в RAG индекс
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional

class KotlinClassExtractor:
    """Извлекает информацию о классах из Kotlin файлов"""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.classes_info = []

    def extract_class_info(self, file_path: Path) -> List[Dict]:
        """Извлекает информацию о классах из одного файла"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except:
            return []

        classes = []
        lines = content.split('\n')

        # Паттерны для поиска классов, интерфейсов, object
        patterns = [
            r'(class|interface|object|data class|sealed class|enum class)\s+(\w+)',
            r'@Composable\s+fun\s+(\w+)',  # Composable функции
        ]

        i = 0
        while i < len(lines):
            line = lines[i].strip()

            # Пропускаем комментарии
            if line.startswith('//') or line.startswith('/*'):
                i += 1
                continue

            # Ищем объявления классов
            for pattern in patterns:
                match = re.search(pattern, line)
                if match:
                    if 'Composable' in pattern:
                        class_type = 'Composable'
                        class_name = match.group(1)
                    else:
                        class_type = match.group(1)
                        class_name = match.group(2)

                    # Собираем документацию и код класса
                    doc_comment = self._extract_doc_comment(lines, i)
                    class_code = self._extract_class_body(lines, i, class_name)

                    relative_path = str(file_path.relative_to(self.project_root))

                    classes.append({
                        'name': class_name,
                        'type': class_type,
                        'file': relative_path,
                        'line': i + 1,
                        'doc': doc_comment,
                        'code': class_code,
                        'full_text': self._format_class_description(
                            class_name, class_type, relative_path,
                            i + 1, doc_comment, class_code
                        )
                    })
                    break

            i += 1

        return classes

    def _extract_doc_comment(self, lines: List[str], start_idx: int) -> str:
        """Извлекает KDoc комментарий перед классом"""
        doc_lines = []
        i = start_idx - 1

        # Ищем комментарий выше
        while i >= 0:
            line = lines[i].strip()
            if line.startswith('/**') or line.startswith('*'):
                doc_lines.insert(0, line.replace('/**', '').replace('*/', '').replace('*', '').strip())
                i -= 1
                if '/**' in lines[i + 1]:
                    break
            elif line == '' or line.startswith('@'):
                i -= 1
            else:
                break

        return ' '.join(doc_lines).strip()

    def _extract_class_body(self, lines: List[str], start_idx: int, class_name: str) -> str:
        """Извлекает тело класса (первые 20 строк или до конца)"""
        class_lines = []
        i = start_idx
        brace_count = 0
        started = False
        max_lines = 30

        while i < len(lines) and len(class_lines) < max_lines:
            line = lines[i]
            class_lines.append(line)

            # Подсчёт скобок
            brace_count += line.count('{') - line.count('}')

            if '{' in line:
                started = True

            # Если закрылись все скобки - конец класса
            if started and brace_count == 0:
                break

            i += 1

        return '\n'.join(class_lines)

    def _format_class_description(self, name: str, type_: str, file: str,
                                   line: int, doc: str, code: str) -> str:
        """Форматирует описание класса для RAG"""
        text = f"# {type_} {name}\n\n"
        text += f"**Файл:** {file}:{line}\n\n"

        if doc:
            text += f"**Описание:** {doc}\n\n"

        text += f"**Код:**\n```kotlin\n{code}\n```\n"

        return text

    def scan_project(self):
        """Сканирует проект и извлекает все классы"""
        print("=== Сканирование проекта для поиска классов ===\n")

        # Ищем Kotlin файлы в app/src
        app_src = self.project_root / "app" / "src" / "main" / "java"

        if not app_src.exists():
            print(f"Директория не найдена: {app_src}")
            return

        kotlin_files = list(app_src.rglob("*.kt"))
        print(f"Найдено Kotlin файлов: {len(kotlin_files)}\n")

        for kt_file in kotlin_files:
            classes = self.extract_class_info(kt_file)
            if classes:
                for cls in classes:
                    self.classes_info.append(cls)
                    print(f"✓ {cls['type']} {cls['name']} ({cls['file']}:{cls['line']})")

        print(f"\n✓ Всего найдено классов: {len(self.classes_info)}")

    def save_to_rag(self, output_file: Path):
        """Сохраняет информацию о классах в формате для RAG"""
        rag_documents = []

        for cls in self.classes_info:
            rag_documents.append({
                'file': f"{cls['file']}:{cls['line']}",
                'chunk_index': 0,
                'content': cls['full_text'],
                'metadata': {
                    'class_name': cls['name'],
                    'class_type': cls['type'],
                    'source_file': cls['file']
                }
            })

        # Сохраняем
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'total_classes': len(rag_documents),
                'documents': rag_documents
            }, f, ensure_ascii=False, indent=2)

        print(f"\n✓ Сохранено в {output_file}")
        return rag_documents


def merge_with_existing_rag(classes_file: Path, rag_index_file: Path):
    """Объединяет индекс классов с существующим RAG индексом"""

    # Загружаем классы
    with open(classes_file, 'r', encoding='utf-8') as f:
        classes_data = json.load(f)

    # Загружаем существующий RAG индекс
    with open(rag_index_file, 'r', encoding='utf-8') as f:
        rag_data = json.load(f)

    # Объединяем
    all_documents = rag_data['documents'] + classes_data['documents']

    merged = {
        'total_documents': len(all_documents),
        'documents': all_documents,
        'metadata': {
            'documentation_chunks': rag_data['total_documents'],
            'code_classes': classes_data['total_classes']
        }
    }

    # Сохраняем обратно
    with open(rag_index_file, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Индексы объединены:")
    print(f"  Документация: {rag_data['total_documents']} чанков")
    print(f"  Классы: {classes_data['total_classes']} классов")
    print(f"  Всего: {len(all_documents)} документов")


def main():
    import sys

    # assistant/ находится в корне проекта, поэтому parent - это корень
    project_root = Path(__file__).parent.parent
    classes_output = project_root / "project" / "docs" / "classes_index.json"
    rag_index = project_root / "project" / "docs" / "rag_index.json"

    extractor = KotlinClassExtractor(project_root)

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "scan":
            # Сканирование и сохранение
            extractor.scan_project()
            extractor.save_to_rag(classes_output)

        elif command == "merge":
            # Объединение с существующим RAG
            if not classes_output.exists():
                print("Сначала запустите: python3 index_classes.py scan")
                return

            merge_with_existing_rag(classes_output, rag_index)

        elif command == "full":
            # Полный цикл: scan + merge
            extractor.scan_project()
            extractor.save_to_rag(classes_output)
            merge_with_existing_rag(classes_output, rag_index)

        else:
            print(f"Неизвестная команда: {command}")

    else:
        print("Индексация классов проекта Movike")
        print("\nКоманды:")
        print("  python3 index_classes.py scan   # Сканировать классы")
        print("  python3 index_classes.py merge  # Объединить с RAG")
        print("  python3 index_classes.py full   # Всё сразу")


if __name__ == "__main__":
    main()
