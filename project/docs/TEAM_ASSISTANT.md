# Team Assistant - Integrated Chat Service

## Overview

The Team Assistant is an integrated service that combines:
- **RAG (Retrieval-Augmented Generation)** for documentation search
- **MCP (Model Context Protocol)** for Git and CRM integration
- **Task Management** with prioritization and recommendations
- **Jetpack Compose** chat interface for Android

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Android App (Kotlin)                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         Jetpack Compose Chat UI                       │  │
│  │  • AssistantChatScreen                                │  │
│  │  • Material Design 3                                  │  │
│  │  • Real-time message updates                          │  │
│  └───────────────────┬───────────────────────────────────┘  │
│                      │                                       │
│  ┌───────────────────┴───────────────────────────────────┐  │
│  │         AssistantChatViewModel                        │  │
│  │  • State management                                   │  │
│  │  • Message handling                                   │  │
│  │  • Error handling                                     │  │
│  └───────────────────┬───────────────────────────────────┘  │
│                      │                                       │
│  ┌───────────────────┴───────────────────────────────────┐  │
│  │         AssistantRepository                           │  │
│  │  • Intent parsing                                     │  │
│  │  • Context aggregation                                │  │
│  │  • Response formatting                                │  │
│  └───────────────────┬───────────────────────────────────┘  │
│                      │                                       │
│  ┌───────────────────┴───────────────────────────────────┐  │
│  │         Ktor HTTP Client                              │  │
│  │  • JSON serialization                                 │  │
│  │  • Network requests                                   │  │
│  │  • Logging                                            │  │
│  └───────────────────┬───────────────────────────────────┘  │
└────────────────────┬─┴───────────────────────────────────────┘
                     │ HTTP/REST API
┌────────────────────┴─────────────────────────────────────────┐
│                Python Backend Service                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │         TeamAssistant (Flask)                         │  │
│  │  • Question answering                                 │  │
│  │  • Intent parsing                                     │  │
│  │  • Context integration                                │  │
│  └──────┬────────────┬────────────┬───────────────────────┘  │
│         │            │            │                          │
│  ┌──────┴─────┐ ┌───┴─────┐ ┌───┴──────────┐               │
│  │    RAG     │ │   MCP   │ │     Tasks    │               │
│  │  System    │ │   Git   │ │  Management  │               │
│  │            │ │ Server  │ │              │               │
│  │ • Index    │ │ • Branch│ │ • CRUD       │               │
│  │ • Search   │ │ • Status│ │ • Priority   │               │
│  │ • Score    │ │ • Files │ │ • Recommend  │               │
│  └────────────┘ └─────────┘ └──────────────┘               │
└──────────────────────────────────────────────────────────────┘
```

## Components

### Android Components

#### 1. Models (`app/src/main/java/dev/kamikaze/movike/models/assistant/`)

- **ChatMessage.kt**: Chat message model with metadata
- **Task.kt**: Task model with priority and status
- **AssistantRequest.kt**: API request/response models

#### 2. Data Layer (`app/src/main/java/dev/kamikaze/movike/data/assistant/`)

- **AssistantApiService.kt**: Ktor-based HTTP client
- **AssistantRepository.kt**: Business logic and intent parsing

#### 3. UI Layer (`app/src/main/java/dev/kamikaze/movike/presentation/ui/compose/assistant/`)

- **AssistantChatScreen.kt**: Main Compose UI
- **AssistantChatViewModel.kt**: State management
- **AssistantChatActivity.kt**: Activity host

#### 4. Dependency Injection (`app/src/main/java/dev/kamikaze/movike/di/modules/`)

- **NetworkModule.kt**: HTTP client configuration
- **AssistantModule.kt**: ViewModel bindings

### Python Backend

#### Main Service (`assistant/team_assistant_service.py`)

**Key Features:**
- Flask REST API server
- Intent-based query routing
- Multi-source context aggregation
- Task management with in-memory storage

**Endpoints:**

```
POST /api/assistant/ask
Body: {
  "question": "Show high priority tasks",
  "context": {
    "includeRAG": true,
    "includeGitContext": true,
    "includeTasks": true,
    "maxResults": 5
  }
}

GET /api/assistant/status
Response: Project status with task statistics

POST /api/tasks/query
Body: {
  "priority": "HIGH",
  "status": "TODO",
  "limit": 10
}

POST /api/tasks/create
Body: {
  "title": "New task",
  "description": "Task description",
  "priority": "MEDIUM",
  "tags": ["backend"]
}

GET /api/rag/search?query=architecture&limit=5
Response: Documentation search results

GET /api/git/context
Response: Current Git branch and status
```

## Setup and Installation

### Prerequisites

- Android Studio Hedgehog or newer
- JDK 17+
- Python 3.7+
- Git

### Backend Setup

1. **Install Python dependencies:**
```bash
pip3 install flask flask-cors
```

2. **Index documentation:**
```bash
cd assistant
python3 simple_rag.py index
```

3. **Start the service:**
```bash
cd ..
./run_team_assistant.sh
```

Or manually:
```bash
cd assistant
python3 team_assistant_service.py --host 0.0.0.0 --port 5001 --load-samples --debug
```

The service will start on `http://localhost:5001`

### Android Setup

1. **Open project in Android Studio:**
```bash
cd /Users/admin/StudioProjects/movike
```

2. **Sync Gradle:**
- Open Android Studio
- Wait for Gradle sync to complete

3. **Build the project:**
```bash
./gradlew assembleDebug
```

4. **Run the app:**
- Select a device/emulator
- Click Run or use: `./gradlew installDebug`

5. **Launch Assistant:**
- From your app, navigate to the Assistant Chat
- Or use Intent:
```kotlin
val intent = Intent(context, AssistantChatActivity::class.java)
startActivity(intent)
```

## Usage Examples

### 1. Query High Priority Tasks

**User:** "Show tasks with high priority"

**Response:**
```
🔥 High Priority Tasks:

1. [HIGH] Implement user authentication
   Status: IN_PROGRESS
   Add JWT-based authentication to the API

2. [HIGH] Optimize database queries
   Status: BLOCKED
   Waiting for database schema approval

💡 Recommendations:
• Focus on 2 high-priority tasks first
• Unblock 1 blocked tasks to improve workflow
```

### 2. Get Project Status

**User:** "What's the project status?"

**Response:**
```
📊 Project Status:

Total tasks: 5

By Priority:
  LOW: 1
  MEDIUM: 1
  HIGH: 2
  CRITICAL: 1

By Status:
  TODO: 2
  IN_PROGRESS: 1
  IN_REVIEW: 1
  BLOCKED: 1

🔥 High Priority Tasks:
  • Implement user authentication
  • Optimize database queries

💡 Recommendations:
  • Focus on 2 high-priority tasks first
  • Unblock 1 blocked tasks to improve workflow
```

### 3. Search Documentation

**User:** "How does the architecture work?"

**Response:**
```
📚 Found relevant documentation:

1. From PROJECT_STRUCTURE.md:
   The project follows Clean Architecture with three main layers:
   - Presentation (UI, ViewModels)
   - Domain (Use Cases, Entities)
   - Data (Repositories, APIs)...

2. From ARCHITECTURE_VERIFICATION.md:
   The architecture is verified through automated tests...
```

### 4. Create a Task

**User:** "Create task: Fix memory leak with high priority. Description: Images not released properly"

The assistant will parse the request and create the task.

### 5. Get Recommendations

**User:** "What should I do first?"

**Response:**
```
💡 Task Recommendations:

Based on current priorities:
1. Start with CRITICAL task: Fix memory leak in image loading
2. Then work on: Implement user authentication
3. Unblock: Optimize database queries

These tasks will have the highest impact on project progress.
```

## Features

### Intent Recognition

The assistant automatically recognizes question intent:

- **Tasks**: "показать задачи", "show tasks", "tasks with high priority"
- **Status**: "project status", "статус проекта", "overview"
- **Priority**: "high priority", "важные задачи", "what's urgent"
- **Documentation**: "how does", "как работает", "documentation about"
- **Git**: "current branch", "git status", "recent commits"
- **General**: Any other questions combine all contexts

### Context Integration

Each response can include:

1. **RAG Context**: Relevant documentation sections
2. **Git Context**: Current branch, modified files, recent commits
3. **Task Context**: Related tasks, priorities, blockers
4. **Recommendations**: AI-generated suggestions

### UI Features

- **Material Design 3**: Modern, adaptive theming
- **Real-time Updates**: Live message streaming
- **Loading States**: Visual feedback during processing
- **Error Handling**: User-friendly error messages
- **Quick Actions**: Pre-defined common queries
- **Metadata Display**: Sources, tasks, and suggestions
- **Dark Mode**: Automatic theme switching

## Configuration

### Backend Configuration

Edit `assistant/team_assistant_service.py`:

```python
# Change port
parser.add_argument('--port', type=int, default=5001)

# Enable/disable features
include_rag = True
include_git = True
include_tasks = True
```

### Android Configuration

Edit `app/src/main/java/dev/kamikaze/movike/data/assistant/AssistantApiService.kt`:

```kotlin
// Change backend URL
private val baseUrl: String = "http://10.0.2.2:5001" // For emulator
// private val baseUrl: String = "http://localhost:5001" // For device
```

## Testing

### Test Backend Service

```bash
# Health check
curl http://localhost:5001/health

# Ask question
curl -X POST http://localhost:5001/api/assistant/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Show high priority tasks"}'

# Get status
curl http://localhost:5001/api/assistant/status

# Query tasks
curl -X POST http://localhost:5001/api/tasks/query \
  -H "Content-Type: application/json" \
  -d '{"priority": "HIGH"}'

# Create task
curl -X POST http://localhost:5001/api/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test task",
    "description": "Test description",
    "priority": "HIGH"
  }'
```

### Test Android App

1. **Start backend service**
2. **Launch app on emulator/device**
3. **Open Assistant Chat**
4. **Try sample queries:**
   - "Show high priority tasks"
   - "What's the project status?"
   - "Search documentation about architecture"
   - "What should I do first?"

## Troubleshooting

### Backend Issues

**Problem:** Service won't start
```bash
# Check Python version
python3 --version  # Should be 3.7+

# Install dependencies
pip3 install flask flask-cors

# Check port availability
lsof -i :5001
```

**Problem:** RAG index not found
```bash
# Re-index documentation
cd assistant
python3 simple_rag.py index
```

### Android Issues

**Problem:** Network error
- For emulator, use `http://10.0.2.2:5001`
- For device, use your computer's IP
- Check backend is running: `curl http://localhost:5001/health`

**Problem:** Compose build errors
- Ensure Kotlin version matches Compose compiler
- Sync Gradle files
- Clean and rebuild: `./gradlew clean build`

**Problem:** Dagger injection errors
- Rebuild project
- Check all modules are included in AppComponent
- Verify @Inject annotations

## Future Enhancements

1. **Persistent Storage**: Replace in-memory tasks with SQLite/Room
2. **Authentication**: Add user authentication and authorization
3. **Real-time Sync**: WebSocket support for live updates
4. **Voice Input**: Speech-to-text integration
5. **Notifications**: Push notifications for task updates
6. **Attachments**: File and image support in chat
7. **Multi-language**: i18n support for multiple languages
8. **Analytics**: Usage tracking and insights
9. **Offline Mode**: Local processing with sync
10. **Export**: Export chat history and reports

## Contributing

When contributing to the Team Assistant:

1. Follow the existing code style
2. Add tests for new features
3. Update documentation
4. Test on both emulator and device
5. Ensure backend compatibility

## License

Same as the main Movike project.

## Support

For issues and questions:
- Check the [troubleshooting section](#troubleshooting)
- Review the [API documentation](#endpoints)
- Open an issue on GitHub
