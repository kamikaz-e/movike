#!/usr/bin/env python3
"""
Простой MCP сервер для получения информации о git ветке
Используется для демонстрации интеграции MCP с проектом
"""

import json
import sys
import subprocess
import xml.etree.ElementTree as ET
import os
from pathlib import Path
from typing import Dict, Any, List


class GitMCPServer:
    """MCP сервер для git операций"""

    def __init__(self):
        self.tools = {
            "git_current_branch": {
                "name": "git_current_branch",
                "description": "Получает имя текущей git ветки",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "git_branch_info": {
                "name": "git_branch_info",
                "description": "Получает детальную информацию о текущей ветке",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            },
            "get_open_files": {
                "name": "get_open_files",
                "description": "Получает список открытых файлов в Android Studio",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        }

    def get_current_branch(self) -> str:
        """Возвращает имя текущей ветки"""
        try:
            result = subprocess.run(
                ['git', 'branch', '--show-current'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return f"Error: {e.stderr}"

    def get_branch_info(self) -> Dict[str, Any]:
        """Возвращает детальную информацию о ветке"""
        try:
            branch = self.get_current_branch()

            # Статус
            status_result = subprocess.run(
                ['git', 'status', '--short', '--branch'],
                capture_output=True,
                text=True,
                check=True
            )

            # Последний коммит
            commit_result = subprocess.run(
                ['git', 'log', '-1', '--oneline'],
                capture_output=True,
                text=True,
                check=True
            )

            # Список веток
            branches_result = subprocess.run(
                ['git', 'branch', '--list'],
                capture_output=True,
                text=True,
                check=True
            )

            return {
                "current_branch": branch,
                "status": status_result.stdout.strip(),
                "last_commit": commit_result.stdout.strip(),
                "all_branches": [
                    b.strip().replace('* ', '')
                    for b in branches_result.stdout.strip().split('\n')
                ]
            }
        except subprocess.CalledProcessError as e:
            return {"error": str(e)}

    def get_recently_modified_files(self, hours: int = 1) -> List[str]:
        """Получает файлы, измененные за последние N часов"""
        try:
            result = subprocess.run(
                ['find', 'app/src/main', '-name', '*.kt', '-mtime', f'-{hours}h', '-type', 'f'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                files = result.stdout.strip().split('\n')
                return [f for f in files if f]
            return []
        except:
            return []

    def get_git_modified_files(self) -> List[str]:
        """Получает файлы с незакоммиченными изменениями из git"""
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD'],
                capture_output=True,
                text=True,
                timeout=5
            )
            modified = result.stdout.strip().split('\n') if result.returncode == 0 else []

            # Также добавляем untracked файлы
            result = subprocess.run(
                ['git', 'ls-files', '--others', '--exclude-standard'],
                capture_output=True,
                text=True,
                timeout=5
            )
            untracked = result.stdout.strip().split('\n') if result.returncode == 0 else []

            # Фильтруем только .kt файлы
            all_files = modified + untracked
            return [f for f in all_files if f.endswith('.kt') and f]
        except:
            return []

    def get_open_files(self) -> Dict[str, Any]:
        """
        Получает список открытых файлов из workspace.xml Android Studio
        С умным fallback'ом на другие источники
        """
        result = {
            'source': 'unknown',
            'files': [],
            'confidence': 'low'
        }

        try:
            # СТРАТЕГИЯ 1: Парсим workspace.xml
            workspace_path = Path('.idea/workspace.xml')

            if workspace_path.exists():
                tree = ET.parse(workspace_path)
                root = tree.getroot()

                open_files = []

                # Ищем FileEditorManager component
                for component in root.findall(".//component[@name='FileEditorManager']"):
                    # Ищем открытые файлы через разные теги
                    for file_elem in component.findall(".//file"):
                        url = file_elem.get('url', '')
                        if url.startswith('file://$PROJECT_DIR$/'):
                            file_path = url.replace('file://$PROJECT_DIR$/', '')
                            if file_path.endswith('.kt'):
                                open_files.append(file_path)

                    for entry in component.findall(".//entry"):
                        file_attr = entry.get('file', '')
                        if file_attr.startswith('file://$PROJECT_DIR$/'):
                            file_path = file_attr.replace('file://$PROJECT_DIR$/', '')
                            if file_path and file_path not in open_files and file_path.endswith('.kt'):
                                open_files.append(file_path)

                if open_files:
                    result['source'] = 'workspace.xml'
                    result['files'] = open_files
                    result['confidence'] = 'high'
                    return result

            # СТРАТЕГИЯ 2: Файлы с незакоммиченными изменениями (git status)
            git_files = self.get_git_modified_files()
            if git_files:
                result['source'] = 'git_modified'
                result['files'] = git_files[:10]  # Ограничиваем 10 файлами
                result['confidence'] = 'medium'
                return result

            # СТРАТЕГИЯ 3: Недавно измененные файлы (последний час)
            recent_1h = self.get_recently_modified_files(hours=1)
            if recent_1h:
                result['source'] = 'recently_modified_1h'
                result['files'] = recent_1h[:10]
                result['confidence'] = 'low'
                return result

            # СТРАТЕГИЯ 4: Файлы за последние 24 часа
            recent_24h = self.get_recently_modified_files(hours=24)
            if recent_24h:
                result['source'] = 'recently_modified_24h'
                result['files'] = recent_24h[:10]
                result['confidence'] = 'very_low'
                return result

            # Если ничего не нашли
            result['source'] = 'none'
            result['files'] = []
            result['confidence'] = 'none'
            return result

        except Exception as e:
            result['source'] = 'error'
            result['files'] = []
            result['confidence'] = 'none'
            result['error'] = str(e)
            return result

    def handle_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Обрабатывает MCP запрос"""
        method = request.get("method")
        params = request.get("params", {})

        if method == "initialize":
            return {
                "protocolVersion": "0.1.0",
                "serverInfo": {
                    "name": "git-mcp-server",
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

            if tool_name == "git_current_branch":
                branch = self.get_current_branch()
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": f"Текущая ветка: {branch}"
                        }
                    ]
                }

            elif tool_name == "git_branch_info":
                info = self.get_branch_info()
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(info, ensure_ascii=False, indent=2)
                        }
                    ]
                }

            elif tool_name == "get_open_files":
                result = self.get_open_files()
                return {
                    "content": [
                        {
                            "type": "text",
                            "text": json.dumps(result, ensure_ascii=False, indent=2)
                        }
                    ]
                }

            return {"error": "Unknown tool"}

        return {"error": "Unknown method"}

    def run(self):
        """Запускает MCP сервер"""
        print("MCP Git Server started", file=sys.stderr)

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
        server = GitMCPServer()

        print("=== Тест MCP Git Server ===\n")

        print("1. Текущая ветка:")
        print(f"   {server.get_current_branch()}\n")

        print("2. Информация о ветке:")
        info = server.get_branch_info()
        print(json.dumps(info, ensure_ascii=False, indent=2))

        print("\n3. Открытые файлы:")
        result = server.get_open_files()
        print(f"   Источник: {result['source']}")
        print(f"   Уверенность: {result['confidence']}")
        print(f"   Найдено файлов: {len(result['files'])}")
        if 'error' in result:
            print(f"   Ошибка: {result['error']}")
        for f in result['files'][:5]:
            print(f"   - {f}")
        if len(result['files']) > 5:
            print(f"   ... и ещё {len(result['files']) - 5} файлов")

    else:
        # Запуск MCP сервера
        server = GitMCPServer()
        server.run()


if __name__ == "__main__":
    main()
