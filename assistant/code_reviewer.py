#!/usr/bin/env python3
"""
AI Code Reviewer для Pull Requests
Анализирует PR используя RAG для контекста и MCP для получения diff
"""

import sys
import os
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Any

# Добавляем текущую директорию в путь для импорта
ASSISTANT_DIR = Path(__file__).parent
sys.path.insert(0, str(ASSISTANT_DIR))

from simple_rag import SimpleRAG
from mcp_git_server import GitMCPServer


class CodeReviewer:
    """Анализатор кода для Pull Requests"""

    def __init__(self, base_branch: str = "main"):
        self.base_branch = base_branch
        self.project_root = ASSISTANT_DIR.parent
        self.rag = SimpleRAG()
        self.git_server = GitMCPServer()

        # Загружаем RAG индекс
        if self.rag.index_path.exists():
            self.rag.load_index()

    def get_pr_context(self) -> Dict[str, Any]:
        """Получает контекст PR через MCP"""
        print("📊 Получение информации о PR...\n")

        # Получаем список измененных файлов
        files_info = self.git_server.get_pr_files(self.base_branch)

        # Получаем diff
        diff_info = self.git_server.get_pr_diff(self.base_branch)

        return {
            'files': files_info.get('files', []),
            'diff': diff_info.get('diff', ''),
            'base': self.base_branch,
            'head': diff_info.get('head', 'HEAD')
        }

    def analyze_file_changes(self, file_path: str, status: str) -> Dict[str, Any]:
        """Анализирует изменения в конкретном файле"""
        analysis = {
            'file': file_path,
            'status': status,
            'issues': [],
            'suggestions': [],
            'potential_bugs': []
        }

        # Получаем содержимое файла
        file_content = self.git_server.get_file_content(file_path)

        if not file_content.get('success'):
            return analysis

        content = file_content.get('content', '')

        # Проверки для Kotlin файлов
        if file_path.endswith('.kt'):
            analysis['issues'].extend(self._check_kotlin_issues(content, file_path))
            analysis['suggestions'].extend(self._check_kotlin_suggestions(content, file_path))
            analysis['potential_bugs'].extend(self._check_kotlin_bugs(content, file_path))

        return analysis

    def _check_kotlin_issues(self, content: str, file_path: str) -> List[str]:
        """Проверяет общие проблемы в Kotlin коде"""
        issues = []

        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Проверка на TODO/FIXME
            if 'TODO' in line or 'FIXME' in line:
                issues.append(f"Line {i}: Найден TODO/FIXME комментарий")

            # Проверка на println (не должно быть в продакшн коде)
            if 'println(' in line and 'test' not in file_path.lower():
                issues.append(f"Line {i}: Использование println() в продакшн коде")

            # Проверка на !! (force unwrap)
            if '!!' in line and '//' not in line[:line.find('!!')]:
                issues.append(f"Line {i}: Использование !! (force unwrap) может привести к NPE")

            # Проверка на пустой catch блок
            if line.strip() == 'catch (e: Exception) {' or line.strip() == 'catch (e: Throwable) {':
                if i < len(lines) and lines[i].strip() == '}':
                    issues.append(f"Line {i}: Пустой catch блок - ошибки игнорируются")

        return issues

    def _check_kotlin_suggestions(self, content: str, file_path: str) -> List[str]:
        """Предлагает улучшения для Kotlin кода"""
        suggestions = []

        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Предложение использовать let/apply/also
            if 'if (' in line and '!= null)' in line:
                suggestions.append(f"Line {i}: Рассмотрите использование ?.let {{ }} вместо if != null")

            # Предложение использовать when вместо множественных if
            if line.strip().startswith('if (') and i + 2 < len(lines):
                next_line = lines[i].strip() if i < len(lines) else ''
                if next_line.startswith('else if ('):
                    suggestions.append(f"Line {i}: При множественных условиях рассмотрите использование when")

            # Предложение использовать const для констант
            if 'val ' in line and line.strip().startswith('val ') and '=' in line:
                if '"' in line or line.split('=')[1].strip().replace('.', '').isdigit():
                    if 'companion object' not in '\n'.join(lines[max(0, i-5):i]):
                        suggestions.append(f"Line {i}: Для констант на уровне файла используйте const val")

        return suggestions

    def _check_kotlin_bugs(self, content: str, file_path: str) -> List[str]:
        """Ищет потенциальные баги в Kotlin коде"""
        bugs = []

        lines = content.split('\n')

        for i, line in enumerate(lines, 1):
            # Потенциальная утечка памяти - обработчики не очищаются
            if 'addListener' in line or 'setOnClickListener' in line:
                bugs.append(f"Line {i}: Убедитесь, что listener очищается в onDestroy/onDestroyView")

            # Использование GlobalScope (антипаттерн)
            if 'GlobalScope.launch' in line:
                bugs.append(f"Line {i}: Использование GlobalScope - рассмотрите lifecycleScope или viewModelScope")

            # Отсутствие Dispatchers в корутинах
            if 'launch {' in line or 'async {' in line:
                if 'Dispatchers' not in line:
                    bugs.append(f"Line {i}: Корутина без явного Dispatcher - может выполняться на UI потоке")

            # Проверка на memory leak в ViewModel
            if 'ViewModel' in content and 'Context' in line and 'Application' not in line:
                if 'private val context' in line.lower() or 'private var context' in line.lower():
                    bugs.append(f"Line {i}: Хранение Context в ViewModel может привести к утечке памяти")

        return bugs

    def search_related_docs(self, file_path: str) -> List[Dict[str, Any]]:
        """Ищет связанную документацию в RAG"""
        if not self.rag.documents:
            return []

        # Извлекаем ключевые слова из пути
        keywords = file_path.replace('/', ' ').replace('.kt', '').replace('_', ' ')

        # Ищем в RAG
        results = self.rag.search(keywords, limit=3)

        return results

    def generate_review(self, pr_context: Dict[str, Any]) -> str:
        """Генерирует текст ревью"""
        print("🔍 Анализ изменений...\n")

        files = pr_context['files']

        if not files:
            return "❌ Не найдено измененных файлов для анализа"

        review = []
        review.append("# 🤖 AI Code Review\n")
        review.append(f"**Base branch:** `{pr_context['base']}`")
        review.append(f"**Head branch:** `{pr_context['head']}`")
        review.append(f"**Files changed:** {len(files)}\n")
        review.append("---\n")

        # Анализируем каждый файл
        total_issues = 0
        total_suggestions = 0
        total_bugs = 0

        for file_info in files:
            file_path = file_info['path']
            status = file_info['status']

            print(f"  Анализирую: {file_path}")

            analysis = self.analyze_file_changes(file_path, status)

            if analysis['issues'] or analysis['suggestions'] or analysis['potential_bugs']:
                review.append(f"## 📄 `{file_path}`\n")
                review.append(f"**Status:** {status}\n")

                if analysis['issues']:
                    total_issues += len(analysis['issues'])
                    review.append("### ⚠️ Проблемы:\n")
                    for issue in analysis['issues']:
                        review.append(f"- {issue}")
                    review.append("")

                if analysis['potential_bugs']:
                    total_bugs += len(analysis['potential_bugs'])
                    review.append("### 🐛 Потенциальные баги:\n")
                    for bug in analysis['potential_bugs']:
                        review.append(f"- {bug}")
                    review.append("")

                if analysis['suggestions']:
                    total_suggestions += len(analysis['suggestions'])
                    review.append("### 💡 Советы по улучшению:\n")
                    for suggestion in analysis['suggestions']:
                        review.append(f"- {suggestion}")
                    review.append("")

                # Добавляем связанную документацию
                docs = self.search_related_docs(file_path)
                if docs:
                    review.append("### 📚 Связанная документация:\n")
                    for doc in docs[:2]:
                        review.append(f"- `{doc['file']}` (релевантность: {doc['score']})")
                    review.append("")

                review.append("---\n")

        # Сводка
        review.append("## 📊 Сводка\n")
        review.append(f"- **Всего проблем:** {total_issues}")
        review.append(f"- **Потенциальных багов:** {total_bugs}")
        review.append(f"- **Предложений по улучшению:** {total_suggestions}\n")

        if total_bugs > 0:
            review.append("### ❗ Рекомендация: Критические проблемы требуют внимания!\n")
        elif total_issues > 5:
            review.append("### ⚠️ Рекомендация: Много замечаний, рассмотрите рефакторинг\n")
        elif total_issues == 0 and total_suggestions == 0:
            review.append("### ✅ Отлично! Серьезных проблем не найдено\n")

        review.append("---")
        review.append("*Автоматическое ревью сгенерировано AI Code Reviewer*")

        return '\n'.join(review)

    def review_pr(self) -> str:
        """Выполняет полное ревью PR"""
        print("\n" + "="*60)
        print("  🤖 AI Code Reviewer для Pull Requests")
        print("="*60 + "\n")

        # Получаем контекст PR
        pr_context = self.get_pr_context()

        # Генерируем ревью
        review = self.generate_review(pr_context)

        return review


def main():
    """Главная функция"""
    base_branch = "main"

    # Проверяем аргументы командной строки
    if len(sys.argv) > 1:
        base_branch = sys.argv[1]

    # Проверяем переменные окружения (для CI)
    if 'GITHUB_BASE_REF' in os.environ:
        base_branch = os.environ['GITHUB_BASE_REF']

    print(f"Base branch: {base_branch}\n")

    # Создаем ревьюер и выполняем анализ
    reviewer = CodeReviewer(base_branch)
    review_text = reviewer.review_pr()

    # Выводим результат
    print("\n" + "="*60)
    print("  📝 Результат ревью")
    print("="*60 + "\n")
    print(review_text)

    # Сохраняем в файл
    output_file = ASSISTANT_DIR / "review_output.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(review_text)

    print(f"\n✅ Ревью сохранено в: {output_file}")

    # Для GitHub Actions - сохраняем в GITHUB_STEP_SUMMARY
    if 'GITHUB_STEP_SUMMARY' in os.environ:
        summary_file = os.environ['GITHUB_STEP_SUMMARY']
        with open(summary_file, 'a', encoding='utf-8') as f:
            f.write(review_text)
        print(f"✅ Ревью добавлено в GitHub Step Summary")


if __name__ == "__main__":
    main()
