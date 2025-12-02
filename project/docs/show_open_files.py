#!/usr/bin/env python3
"""
Скрипт для получения и отображения информации об открытых файлах
"""

import subprocess
import json
import sys
from pathlib import Path

def get_open_files():
    """Получает список открытых файлов через MCP сервер"""
    try:
        result = subprocess.run(
            ['python3', 'project/docs/mcp_git_server.py', 'test'],
            capture_output=True,
            text=True,
            timeout=10
        )

        # Парсим вывод и извлекаем файлы
        output = result.stdout

        if '3. Открытые файлы:' in output:
            lines = output.split('\n')
            files = []
            capture = False

            for line in lines:
                if '3. Открытые файлы:' in line:
                    capture = True
                    continue
                if capture and line.strip().startswith('- '):
                    file_path = line.strip()[2:]  # Убираем "- "
                    files.append(file_path)

            return files
        return []

    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        return []

def analyze_file(file_path):
    """Анализирует файл и возвращает краткую информацию"""
    path = Path(file_path)

    if not path.exists():
        return f"Файл не найден: {file_path}"

    try:
        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        # Базовая информация
        info = {
            'path': file_path,
            'lines': len(lines),
            'name': path.name,
            'type': 'Unknown'
        }

        # Определяем тип файла
        content = ''.join(lines)

        if 'class ' in content and 'ViewModel' in file_path:
            info['type'] = 'ViewModel'
        elif 'interface ' in content or ('class ' in content and 'Repository' in file_path):
            info['type'] = 'Repository/Interface'
        elif '@Module' in content or 'Module' in file_path:
            info['type'] = 'Dagger Module'
        elif 'Fragment' in file_path:
            info['type'] = 'Fragment'
        elif 'Activity' in file_path:
            info['type'] = 'Activity'
        elif 'Service' in file_path or 'ApiService' in content:
            info['type'] = 'Service'
        elif 'data class' in content:
            info['type'] = 'Data Class'

        # Извлекаем первые несколько строк (без пустых и комментариев)
        preview_lines = []
        for line in lines[:20]:
            stripped = line.strip()
            if stripped and not stripped.startswith('//') and not stripped.startswith('/*') and not stripped.startswith('*'):
                preview_lines.append(stripped)
                if len(preview_lines) >= 5:
                    break

        info['preview'] = preview_lines

        return info

    except Exception as e:
        return f"Ошибка чтения файла: {e}"

def main():
    print("=== Открытые файлы в Android Studio ===\n")

    files = get_open_files()

    if not files:
        print("Открытые файлы не найдены или используются недавно измененные файлы")
        return

    print(f"Найдено открытых файлов: {len(files)}\n")

    for idx, file_path in enumerate(files, 1):
        info = analyze_file(file_path)

        if isinstance(info, str):
            print(f"{idx}. {info}")
            continue

        print(f"{idx}. {info['name']}")
        print(f"   Тип: {info['type']}")
        print(f"   Путь: {info['path']}")
        print(f"   Строк: {info['lines']}")
        print(f"   Превью:")
        for line in info['preview']:
            print(f"      {line}")
        print()

if __name__ == "__main__":
    main()
