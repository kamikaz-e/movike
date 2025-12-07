#!/usr/bin/env python3
"""
Team Assistant Service
Integrated service combining RAG, MCP (Git & CRM), and Task Management
"""

import json
import logging
import sys
from datetime import datetime
from typing import List, Dict, Any, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS

# Import existing modules
from simple_rag import SimpleRAG
from mcp_git_server import GitMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
# Configure CORS to allow all origins, methods, and headers
# This is needed for Android app to connect properly
CORS(app, 
     resources={r"/api/*": {
         "origins": "*",
         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         "allow_headers": ["Content-Type", "Authorization", "Accept"],
         "expose_headers": ["Content-Type"]
     }},
     supports_credentials=True)

# Initialize components
rag_system = SimpleRAG()
git_server = GitMCPServer()

# In-memory task storage (in production, use a database)
tasks_db: List[Dict[str, Any]] = []
task_counter = 1


class TeamAssistant:
    """
    Integrated Team Assistant that combines:
    - RAG for documentation search
    - MCP Git for repository context
    - Task management with prioritization
    """

    def __init__(self):
        self.rag = rag_system
        self.git_server = git_server

    def ask_question(
        self,
        question: str,
        include_rag: bool = True,
        include_git: bool = True,
        include_tasks: bool = True,
        max_results: int = 5
    ) -> Dict[str, Any]:
        """
        Answer a question with full context from all sources
        """
        answer_parts = []
        sources = []
        related_tasks = []
        suggestions = []
        git_context = None

        try:
            # Analyze question intent
            intent = self._parse_intent(question)
            logger.info(f"Question intent: {intent}")

            # Get RAG context if relevant
            if include_rag and intent in ['documentation', 'general', 'architecture']:
                rag_results = self.rag.search(question, limit=max_results)
                if rag_results:
                    sources = [
                        {
                            'file': r['file'],
                            'content': r['text'][:300],
                            'score': r['score']
                        }
                        for r in rag_results
                    ]
                    answer_parts.append(f"📚 Found {len(sources)} relevant documentation sections.")

            # Get Git context if relevant
            if include_git and intent in ['git', 'code', 'general']:
                git_context = self._get_git_context()
                if git_context:
                    answer_parts.append(
                        f"🔀 Current branch: {git_context['currentBranch']}"
                    )

            # Get task context if relevant (but not for create_task intent)
            if include_tasks and intent in ['tasks', 'priority', 'status', 'general']:
                related_tasks = self._find_related_tasks(question)
                if related_tasks:
                    answer_parts.append(
                        f"📋 Found {len(related_tasks)} related tasks."
                    )

            # Generate specific answer based on intent
            if intent == 'create_task':
                # For task creation, we don't need related tasks context
                answer = self._handle_create_task(question)
                # Get the created task for related_tasks if needed
                if tasks_db:
                    related_tasks = [tasks_db[-1]]  # The just-created task
            elif intent == 'tasks':
                answer = self._handle_task_query(question, related_tasks)
            elif intent == 'status':
                answer = self._handle_status_query()
            elif intent == 'priority':
                answer = self._handle_priority_query()
            elif intent == 'documentation':
                answer = self._handle_documentation_query(sources)
            else:
                answer = self._handle_general_query(
                    question, sources, git_context, related_tasks
                )

            # Generate suggestions
            suggestions = self._generate_suggestions(intent, related_tasks)

            return {
                'answer': answer,
                'sources': sources,
                'relatedTasks': related_tasks,
                'suggestions': suggestions,
                'gitContext': git_context
            }

        except Exception as e:
            logger.error(f"Error answering question: {e}", exc_info=True)
            return {
                'answer': f"Sorry, I encountered an error: {str(e)}",
                'sources': [],
                'relatedTasks': [],
                'suggestions': [],
                'gitContext': None
            }

    def _parse_intent(self, question: str) -> str:
        """Parse user intent from question"""
        q = question.lower()

        # Check for task creation intent first (more specific)
        # Look for patterns like "create task:", "add task:", "new task:"
        create_patterns = [
            r'create\s+task\s*:',
            r'add\s+task\s*:',
            r'new\s+task\s*:',
            r'создать\s+задач',
            r'добавить\s+задач',
        ]
        
        import re
        for pattern in create_patterns:
            if re.search(pattern, q, re.IGNORECASE):
                return 'create_task'
        
        # Also check for phrases without colon
        if any(phrase in q for phrase in ['create task', 'add task', 'new task', 'создать задач', 'добавить задач']):
            return 'create_task'
        elif any(word in q for word in ['задач', 'task', 'todo']):
            return 'tasks'
        elif any(word in q for word in ['статус', 'status', 'overview']):
            return 'status'
        elif any(word in q for word in ['приоритет', 'priority', 'important', 'urgent']):
            return 'priority'
        elif any(word in q for word in ['документац', 'documentation', 'docs', 'как работает']):
            return 'documentation'
        elif any(word in q for word in ['git', 'branch', 'commit', 'код', 'code']):
            return 'git'
        elif any(word in q for word in ['архитектур', 'architecture', 'структур', 'structure']):
            return 'architecture'
        else:
            return 'general'

    def _get_git_context(self) -> Optional[Dict[str, Any]]:
        """Get current Git context"""
        try:
            result = self.git_server.git_branch_info()
            if result:
                return {
                    'currentBranch': result.get('current_branch', ''),
                    'recentCommits': result.get('recent_commits', [])[:5],
                    'modifiedFiles': result.get('modified_files', [])[:10],
                    'status': result.get('status', '')
                }
        except Exception as e:
            logger.error(f"Error getting git context: {e}")
        return None

    def _find_related_tasks(self, question: str) -> List[Dict[str, Any]]:
        """Find tasks related to the question"""
        q = question.lower()
        related = []

        for task in tasks_db:
            # Simple keyword matching
            if (q in task['title'].lower() or
                q in task['description'].lower() or
                any(tag.lower() in q for tag in task.get('tags', []))):
                related.append(task)

        # Also include high priority tasks if question is about priorities
        if 'priority' in q or 'important' in q or 'приоритет' in q:
            high_priority = [
                t for t in tasks_db
                if t['priority'] in ['HIGH', 'CRITICAL']
            ]
            related.extend(high_priority)

        # Remove duplicates
        seen = set()
        unique_related = []
        for task in related:
            if task['id'] not in seen:
                seen.add(task['id'])
                unique_related.append(task)

        return unique_related[:5]

    def _handle_create_task(self, question: str) -> str:
        """Handle task creation from natural language"""
        global task_counter, tasks_db

        try:
            logger.info(f"Processing task creation request: {question}")
            # Parse task details from the question
            task_info = self._parse_task_from_text(question)
            
            # Validate parsed data
            if not task_info.get('title'):
                logger.warning(f"Could not extract title from: {question}")
                return "Sorry, I couldn't extract a task title from your message. Please use format: 'Create task: [Title] with [priority] priority. Description: [description]'"

            # Create the task
            task = {
                'id': str(task_counter),
                'title': task_info['title'],
                'description': task_info['description'],
                'priority': task_info['priority'],
                'status': 'TODO',
                'assignee': task_info.get('assignee'),
                'createdAt': int(datetime.now().timestamp() * 1000),
                'updatedAt': int(datetime.now().timestamp() * 1000),
                'dueDate': task_info.get('dueDate'),
                'tags': task_info.get('tags', [])
            }

            tasks_db.append(task)
            task_counter += 1

            logger.info(f"Created task via chat: {task['id']} - {task['title']}")

            result = [
                f"✅ Task created successfully!\n\n",
                f"ID: {task['id']}\n",
                f"Title: {task['title']}\n",
                f"Description: {task['description']}\n",
                f"Priority: {task['priority']}\n",
                f"Status: {task['status']}\n"
            ]

            if task['assignee']:
                result.append(f"Assignee: {task['assignee']}\n")

            return "".join(result)

        except Exception as e:
            logger.error(f"Error creating task from text: {e}", exc_info=True)
            return f"Sorry, I couldn't create the task. Error: {str(e)}\n\nPlease try a format like: 'Create task: [Title] with [priority] priority. Description: [description]'"

    def _parse_task_from_text(self, text: str) -> Dict[str, Any]:
        """Parse task details from natural language text"""
        import re

        # Default values
        task_info = {
            'title': '',
            'description': '',
            'priority': 'MEDIUM',
            'assignee': None,
            'tags': []
        }

        # First, extract priority (before parsing title/description)
        priority_map = {
            'low': 'LOW',
            'medium': 'MEDIUM',
            'high': 'HIGH',
            'critical': 'CRITICAL'
        }

        text_lower = text.lower()
        for key, value in priority_map.items():
            if key in text_lower:
                task_info['priority'] = value
                break

        # Split text by "Description:" or "description:" to separate title and description
        desc_match = re.search(r'(?:description|desc):\s*', text, re.IGNORECASE)
        
        if desc_match:
            # There's a description section
            desc_start = desc_match.end()
            
            # Title is everything between "Create task:" and "Description:"
            title_end = desc_match.start()
            title_section = text[:title_end]
            
            # Description is everything after "Description:"
            description_section = text[desc_start:].strip()
            
            # Extract title from title_section
            title_patterns = [
                r'(?:create|add|new)\s+task:\s*(.+?)(?:\s+with\s+(?:low|medium|high|critical)\s+priority|$)',
                r'(?:create|add|new)\s+task:\s*(.+?)(?:\s*\.|$)',
                r'(?:create|add|new)\s+task:\s*(.+)',
            ]
            
            for pattern in title_patterns:
                match = re.search(pattern, title_section, re.IGNORECASE)
                if match:
                    task_info['title'] = match.group(1).strip()
                    break
            
            # Clean title - remove priority mentions
            task_info['title'] = re.sub(r'\s+with\s+(low|medium|high|critical)\s+priority', '', task_info['title'], flags=re.IGNORECASE)
            task_info['title'] = task_info['title'].strip().rstrip('.')
            
            # Description is already extracted
            task_info['description'] = description_section.strip().rstrip(',').strip()
            
        else:
            # No explicit description section - extract title and use it as description too
            title_patterns = [
                r'(?:create|add|new)\s+task:\s*(.+?)(?:\s+with\s+(?:low|medium|high|critical)\s+priority|$)',
                r'(?:create|add|new)\s+task:\s*(.+?)(?:\s*\.|$)',
                r'(?:create|add|new)\s+task:\s*(.+)',
            ]
            
            for pattern in title_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    task_info['title'] = match.group(1).strip()
                    break
            
            # If no pattern matched, try simple extraction
            if not task_info['title']:
                match = re.search(r'(?:create|add|new)\s+task:\s*(.+)', text, re.IGNORECASE)
                if match:
                    task_info['title'] = match.group(1).strip()
            
            # Clean title - remove priority mentions
            task_info['title'] = re.sub(r'\s+with\s+(low|medium|high|critical)\s+priority', '', task_info['title'], flags=re.IGNORECASE)
            task_info['title'] = task_info['title'].strip().rstrip('.')
            
            # Use title as description if no description found
            task_info['description'] = task_info['title'] if task_info['title'] else text

        # Final cleanup - remove trailing commas and dots
        task_info['title'] = task_info['title'].strip().rstrip(',').rstrip('.').strip()
        task_info['description'] = task_info['description'].strip().rstrip(',').rstrip('.').strip()
        
        # Ensure we have at least a title
        if not task_info['title']:
            # Fallback: use everything after "create task:" as title
            match = re.search(r'(?:create|add|new)\s+task:?\s*(.+)', text, re.IGNORECASE)
            if match:
                task_info['title'] = match.group(1).strip().rstrip(',').rstrip('.').strip()
                if not task_info['description']:
                    task_info['description'] = task_info['title']

        logger.info(f"Parsed task: title='{task_info['title']}', description='{task_info['description']}', priority='{task_info['priority']}'")
        
        return task_info

    def _handle_task_query(self, question: str, related_tasks: List[Dict]) -> str:
        """Handle task-related queries"""
        if not related_tasks:
            return "No tasks found matching your query. Would you like to create a new task?"

        result = ["Here are the relevant tasks:\n"]
        for i, task in enumerate(related_tasks, 1):
            result.append(
                f"{i}. [{task['priority']}] {task['title']}\n"
                f"   Status: {task['status']}\n"
                f"   {task['description']}\n"
            )

        recommendations = self._get_task_recommendations()
        if recommendations:
            result.append("\n💡 Recommendations:\n")
            for rec in recommendations:
                result.append(f"• {rec}\n")

        return "".join(result)

    def _handle_status_query(self) -> str:
        """Handle project status queries"""
        status = self.get_project_status()

        result = [
            "📊 Project Status:\n\n",
            f"Total tasks: {status['totalTasks']}\n\n",
            "By Priority:\n"
        ]

        for priority, count in status['tasksByPriority'].items():
            result.append(f"  {priority}: {count}\n")

        result.append("\nBy Status:\n")
        for task_status, count in status['tasksByStatus'].items():
            result.append(f"  {task_status}: {count}\n")

        if status['highPriorityTasks']:
            result.append("\n🔥 High Priority Tasks:\n")
            for task in status['highPriorityTasks'][:3]:
                result.append(f"  • {task['title']}\n")

        if status['recommendations']:
            result.append("\n💡 Recommendations:\n")
            for rec in status['recommendations']:
                result.append(f"  • {rec}\n")

        return "".join(result)

    def _handle_priority_query(self) -> str:
        """Handle priority-related queries"""
        high_priority = [t for t in tasks_db if t['priority'] in ['HIGH', 'CRITICAL']]

        if not high_priority:
            return "Great! No high-priority tasks at the moment."

        high_priority.sort(
            key=lambda t: ('CRITICAL', 'HIGH').index(t['priority'])
        )

        result = ["🔥 High Priority Tasks:\n\n"]
        for i, task in enumerate(high_priority[:5], 1):
            result.append(
                f"{i}. [{task['priority']}] {task['title']}\n"
                f"   Status: {task['status']}\n"
                f"   {task['description']}\n\n"
            )

        recommendations = self._prioritize_tasks(high_priority)
        if recommendations:
            result.append("💡 What to do first:\n")
            for rec in recommendations:
                result.append(f"• {rec}\n")

        return "".join(result)

    def _handle_documentation_query(self, sources: List[Dict]) -> str:
        """Handle documentation search queries"""
        if not sources:
            return "No relevant documentation found. Try rephrasing your question."

        result = ["📚 Found relevant documentation:\n\n"]
        for i, source in enumerate(sources, 1):
            result.append(
                f"{i}. From {source['file']}:\n"
                f"   {source['content'][:200]}...\n\n"
            )

        return "".join(result)

    def _handle_general_query(
        self,
        question: str,
        sources: List[Dict],
        git_context: Optional[Dict],
        related_tasks: List[Dict]
    ) -> str:
        """Handle general queries with all available context"""
        result = []

        if sources:
            result.append("📚 From documentation:\n")
            result.append(sources[0]['content'][:300] + "...\n\n")

        if git_context:
            result.append(f"🔀 Current branch: {git_context['currentBranch']}\n")
            if git_context['modifiedFiles']:
                result.append(
                    f"Modified files: {len(git_context['modifiedFiles'])}\n\n"
                )

        if related_tasks:
            result.append(f"📋 Related tasks: {len(related_tasks)}\n\n")

        if not result:
            result.append(
                "I understand your question, but I need more context. "
                "Could you provide more details?\n"
            )

        return "".join(result)

    def _generate_suggestions(
        self,
        intent: str,
        related_tasks: List[Dict]
    ) -> List[str]:
        """Generate helpful suggestions based on context"""
        suggestions = []

        if intent == 'tasks' and related_tasks:
            suggestions.append("Update task status")
            suggestions.append("Show all high priority tasks")

        elif intent == 'status':
            suggestions.append("Show blocked tasks")
            suggestions.append("What should I do first?")

        elif intent == 'priority':
            suggestions.append("Show all tasks")
            suggestions.append("Create new task")

        elif intent == 'documentation':
            suggestions.append("Show project structure")
            suggestions.append("Explain architecture")

        return suggestions

    def _get_task_recommendations(self) -> List[str]:
        """Get task recommendations"""
        recommendations = []

        high_priority = [t for t in tasks_db if t['priority'] in ['HIGH', 'CRITICAL']]
        blocked = [t for t in tasks_db if t['status'] == 'BLOCKED']
        in_review = [t for t in tasks_db if t['status'] == 'IN_REVIEW']

        if high_priority:
            recommendations.append(
                f"Focus on {len(high_priority)} high-priority tasks first"
            )

        if blocked:
            recommendations.append(
                f"Unblock {len(blocked)} blocked tasks to improve workflow"
            )

        if in_review:
            recommendations.append(
                f"Review {len(in_review)} tasks waiting for review"
            )

        return recommendations

    def _prioritize_tasks(self, tasks: List[Dict]) -> List[str]:
        """Prioritize tasks and provide recommendations"""
        if not tasks:
            return []

        recommendations = []

        # Critical tasks first
        critical = [t for t in tasks if t['priority'] == 'CRITICAL']
        if critical:
            recommendations.append(
                f"Start with CRITICAL task: {critical[0]['title']}"
            )

        # Then high priority
        high = [t for t in tasks if t['priority'] == 'HIGH']
        if high and len(recommendations) < 3:
            for task in high[:3 - len(recommendations)]:
                recommendations.append(f"Then work on: {task['title']}")

        return recommendations

    def get_project_status(self) -> Dict[str, Any]:
        """Get comprehensive project status"""
        total_tasks = len(tasks_db)

        # Count by priority
        by_priority = {}
        for priority in ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']:
            by_priority[priority] = len([
                t for t in tasks_db if t['priority'] == priority
            ])

        # Count by status
        by_status = {}
        for status in ['TODO', 'IN_PROGRESS', 'IN_REVIEW', 'DONE', 'BLOCKED']:
            by_status[status] = len([
                t for t in tasks_db if t['status'] == status
            ])

        # Get high priority tasks
        high_priority_tasks = [
            t for t in tasks_db
            if t['priority'] in ['HIGH', 'CRITICAL']
        ]

        # Get blocked tasks
        blocked_tasks = [
            t for t in tasks_db
            if t['status'] == 'BLOCKED'
        ]

        # Generate recommendations
        recommendations = self._get_task_recommendations()

        return {
            'totalTasks': total_tasks,
            'tasksByPriority': by_priority,
            'tasksByStatus': by_status,
            'highPriorityTasks': high_priority_tasks,
            'blockedTasks': blocked_tasks,
            'recommendations': recommendations
        }


# Initialize assistant
assistant = TeamAssistant()


# Global request handlers
@app.before_request
def log_request_info():
    """Log request information for debugging"""
    if request.method != 'OPTIONS':  # Skip logging OPTIONS requests
        logger.info(f"{request.method} {request.path}")
        if request.is_json:
            logger.debug(f"Request JSON: {request.get_json()}")
        elif request.data:
            logger.debug(f"Request data: {request.data.decode('utf-8')[:200]}")


@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response


# REST API Endpoints

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'team-assistant'}), 200


@app.route('/api/assistant/ask', methods=['POST', 'OPTIONS'])
def ask_question():
    """Ask the assistant a question"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        data = request.get_json()
        if data is None and request.data:
            try:
                data = json.loads(request.data.decode('utf-8'))
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {e}")
                return jsonify({'error': 'Invalid JSON format'}), 400
        
        question = data.get('question', '') if data else ''
        context = data.get('context', {}) if data else {}

        if not question:
            return jsonify({'error': 'Question is required'}), 400

        result = assistant.ask_question(
            question=question,
            include_rag=context.get('includeRAG', True),
            include_git=context.get('includeGitContext', True),
            include_tasks=context.get('includeTasks', True),
            max_results=context.get('maxResults', 5)
        )

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in ask_question: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/assistant/status', methods=['GET'])
def get_status():
    """Get project status"""
    try:
        status = assistant.get_project_status()
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Error in get_status: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/query', methods=['POST', 'OPTIONS'])
def query_tasks():
    """Query tasks with filters"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200
    
    try:
        # Log request for debugging
        logger.info(f"Received query_tasks request: {request.method}")
        logger.info(f"Request headers: {dict(request.headers)}")
        
        data = request.get_json()
        if data is None:
            # Try to parse as raw JSON if get_json() returns None
            if request.data:
                try:
                    data = json.loads(request.data.decode('utf-8'))
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse JSON: {e}")
                    return jsonify({'error': 'Invalid JSON format'}), 400
            else:
                return jsonify({'error': 'No data provided'}), 400
        
        logger.info(f"Parsed data: {data}")
        
        priority = data.get('priority')
        status = data.get('status')
        assignee = data.get('assignee')
        tags = data.get('tags', [])
        limit = data.get('limit', 10)

        filtered_tasks = tasks_db.copy()

        if priority:
            filtered_tasks = [t for t in filtered_tasks if t['priority'] == priority]

        if status:
            filtered_tasks = [t for t in filtered_tasks if t['status'] == status]

        if assignee:
            filtered_tasks = [t for t in filtered_tasks if t.get('assignee') == assignee]

        if tags:
            filtered_tasks = [
                t for t in filtered_tasks
                if any(tag in t.get('tags', []) for tag in tags)
            ]

        result = filtered_tasks[:limit]
        logger.info(f"Returning {len(result)} tasks")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Error in query_tasks: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/create', methods=['POST', 'OPTIONS'])
def create_task():
    """Create a new task"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    global task_counter
    try:
        # Log request for debugging
        logger.info(f"Received create_task request")
        logger.info(f"Request headers: {dict(request.headers)}")

        data = request.get_json()
        if data is None and request.data:
            try:
                data = json.loads(request.data.decode('utf-8'))
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {e}")
                return jsonify({'error': 'Invalid JSON format'}), 400

        if data is None:
            logger.error("No data provided")
            return jsonify({'error': 'No data provided'}), 400

        logger.info(f"Parsed data: {data}")

        # Validate required fields
        if not data.get('title'):
            return jsonify({'error': 'Title is required'}), 400

        task = {
            'id': str(task_counter),
            'title': data.get('title', ''),
            'description': data.get('description', ''),
            'priority': data.get('priority', 'MEDIUM'),
            'status': 'TODO',
            'assignee': data.get('assignee'),
            'createdAt': int(datetime.now().timestamp() * 1000),
            'updatedAt': int(datetime.now().timestamp() * 1000),
            'dueDate': data.get('dueDate'),
            'tags': data.get('tags', [])
        }

        tasks_db.append(task)
        task_counter += 1

        logger.info(f"Created task: {task['id']} - {task['title']}")
        return jsonify(task), 201

    except Exception as e:
        logger.error(f"Error in create_task: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/assistant/recommendations', methods=['GET'])
def get_recommendations():
    """Get task recommendations"""
    try:
        recommendations = assistant._get_task_recommendations()
        return jsonify(recommendations), 200
    except Exception as e:
        logger.error(f"Error in get_recommendations: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/rag/search', methods=['GET'])
def search_documentation():
    """Search documentation using RAG"""
    try:
        query = request.args.get('query', '')
        limit = int(request.args.get('limit', 5))

        if not query:
            return jsonify({'error': 'Query is required'}), 400

        results = rag_system.search(query, limit=limit)

        sources = [
            {
                'file': r['file'],
                'content': r['text'],
                'score': r['score']
            }
            for r in results
        ]

        return jsonify(sources), 200

    except Exception as e:
        logger.error(f"Error in search_documentation: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@app.route('/api/git/context', methods=['GET'])
def get_git_context():
    """Get Git context"""
    try:
        context = assistant._get_git_context()
        if context:
            return jsonify(context), 200
        else:
            return jsonify({'error': 'Could not retrieve git context'}), 500
    except Exception as e:
        logger.error(f"Error in get_git_context: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500


def load_sample_tasks():
    """Load sample tasks for testing"""
    global tasks_db, task_counter

    sample_tasks = [
        {
            'id': '1',
            'title': 'Implement user authentication',
            'description': 'Add JWT-based authentication to the API',
            'priority': 'HIGH',
            'status': 'IN_PROGRESS',
            'assignee': 'developer1',
            'createdAt': int(datetime.now().timestamp() * 1000),
            'updatedAt': int(datetime.now().timestamp() * 1000),
            'tags': ['backend', 'security']
        },
        {
            'id': '2',
            'title': 'Fix memory leak in image loading',
            'description': 'Images are not being released from memory properly',
            'priority': 'CRITICAL',
            'status': 'TODO',
            'assignee': 'developer2',
            'createdAt': int(datetime.now().timestamp() * 1000),
            'updatedAt': int(datetime.now().timestamp() * 1000),
            'tags': ['android', 'performance', 'bug']
        },
        {
            'id': '3',
            'title': 'Update UI documentation',
            'description': 'Add screenshots and examples to UI component docs',
            'priority': 'LOW',
            'status': 'TODO',
            'assignee': None,
            'createdAt': int(datetime.now().timestamp() * 1000),
            'updatedAt': int(datetime.now().timestamp() * 1000),
            'tags': ['documentation', 'ui']
        },
        {
            'id': '4',
            'title': 'Add dark mode support',
            'description': 'Implement dark theme across all screens',
            'priority': 'MEDIUM',
            'status': 'IN_REVIEW',
            'assignee': 'developer1',
            'createdAt': int(datetime.now().timestamp() * 1000),
            'updatedAt': int(datetime.now().timestamp() * 1000),
            'tags': ['ui', 'feature']
        },
        {
            'id': '5',
            'title': 'Optimize database queries',
            'description': 'Waiting for database schema approval',
            'priority': 'HIGH',
            'status': 'BLOCKED',
            'assignee': 'developer2',
            'createdAt': int(datetime.now().timestamp() * 1000),
            'updatedAt': int(datetime.now().timestamp() * 1000),
            'tags': ['backend', 'performance']
        }
    ]

    tasks_db = sample_tasks
    task_counter = 6


def main():
    """Main entry point"""
    import argparse

    parser = argparse.ArgumentParser(description='Team Assistant Service')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=5001, help='Port to bind to')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--load-samples', action='store_true', help='Load sample tasks')

    args = parser.parse_args()

    # Load sample data if requested
    if args.load_samples:
        load_sample_tasks()
        logger.info("Loaded sample tasks")

    # Index documentation
    try:
        logger.info("Indexing documentation...")
        rag_system.index_files()
        logger.info("Documentation indexed successfully")
    except Exception as e:
        logger.error(f"Failed to index documentation: {e}")

    # Start server
    logger.info(f"Starting Team Assistant Service on {args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


if __name__ == '__main__':
    main()
