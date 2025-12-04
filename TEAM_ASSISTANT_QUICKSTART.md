# Team Assistant - Quick Start Guide

## 🚀 Quick Start (5 minutes)

### Step 1: Start the Backend (1 minute)

```bash
cd /Users/admin/StudioProjects/movike
./run_team_assistant.sh
```

The service will:
- ✅ Index project documentation
- ✅ Load sample tasks
- ✅ Start on http://localhost:5001

You should see:
```
🤖 Starting Team Assistant Service...
📚 Indexing documentation...
🚀 Starting service on http://localhost:5001
```

### Step 2: Test the Backend (30 seconds)

Open a new terminal:

```bash
# Quick test
curl http://localhost:5001/health
# Should return: {"status":"healthy","service":"team-assistant"}

# Test a question
curl -X POST http://localhost:5001/api/assistant/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "Show high priority tasks"}'
```

### Step 3: Build Android App (2 minutes)

```bash
# In Android Studio:
# 1. Open the project
# 2. Wait for Gradle sync
# 3. Click "Run" or press Shift+F10

# Or via command line:
./gradlew assembleDebug
./gradlew installDebug
```

### Step 4: Launch Assistant in App

Add this code to any Activity/Fragment where you want to launch the assistant:

```kotlin
// Launch Assistant Chat
val intent = Intent(this, AssistantChatActivity::class.java)
startActivity(intent)
```

Or create a test button:

```kotlin
// In your layout or Compose UI
Button(onClick = {
    val intent = Intent(context, AssistantChatActivity::class.java)
    context.startActivity(intent)
}) {
    Text("Open Team Assistant")
}
```

## 📱 Using the Assistant

### Example Queries

Try these questions in the chat:

1. **Task Management:**
   - "Show high priority tasks"
   - "What tasks are blocked?"
   - "Create task: Fix navigation bug"
   - "What should I do first?"

2. **Project Status:**
   - "What's the project status?"
   - "Show me an overview"
   - "How many tasks do we have?"

3. **Documentation:**
   - "How does the architecture work?"
   - "Search documentation about API"
   - "Explain the project structure"

4. **Git Context:**
   - "What branch am I on?"
   - "Show recent commits"
   - "What files changed?"

5. **Recommendations:**
   - "What should I prioritize?"
   - "Give me recommendations"
   - "What's most important?"

## 🎯 Key Features

### 1. Intent Recognition
The assistant automatically understands what you're asking for:
- 📋 Tasks queries → Shows filtered tasks
- 📊 Status queries → Project overview
- 📚 Documentation → RAG search
- 🔀 Git queries → Repository info
- 💡 General → Combines all contexts

### 2. Smart Recommendations
Based on task priorities and statuses:
- Suggests what to work on first
- Identifies blockers
- Highlights critical items
- Recommends workflow improvements

### 3. Multi-Source Context
Each answer can include:
- Documentation excerpts (RAG)
- Related tasks
- Git branch info
- Actionable suggestions

## 🔧 Configuration

### Change Backend URL (for physical device)

Edit `AssistantApiService.kt`:

```kotlin
// For emulator:
private val baseUrl: String = "http://10.0.2.2:5001"

// For physical device (replace with your computer's IP):
private val baseUrl: String = "http://192.168.1.XXX:5001"
```

Find your IP:
```bash
# macOS/Linux:
ifconfig | grep "inet "

# Windows:
ipconfig
```

### Add Sample Tasks

The service auto-loads 5 sample tasks. Add more via API:

```bash
curl -X POST http://localhost:5001/api/tasks/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Your task title",
    "description": "Task description",
    "priority": "HIGH",
    "tags": ["backend", "api"]
  }'
```

### Customize RAG Index

Add your own documentation to be searchable:

```bash
# Add markdown files to:
project/docs/*.md

# Re-index:
cd assistant
python3 simple_rag.py index
```

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Python version (need 3.7+)
python3 --version

# Install dependencies
pip3 install flask flask-cors

# Check port is free
lsof -i :5001
# If occupied, kill with: kill -9 <PID>
```

### Android can't connect to backend

```bash
# 1. Check backend is running
curl http://localhost:5001/health

# 2. For emulator, use: http://10.0.2.2:5001
# 3. For device, check firewall allows connections
# 4. Verify device and computer on same network
```

### Build errors

```bash
# Clean and rebuild
./gradlew clean
./gradlew assembleDebug

# If Compose errors, check:
# - Kotlin version: 1.9.24
# - Compose compiler: 1.5.14
# - Gradle sync completed
```

### No responses from assistant

```bash
# 1. Check backend logs for errors
# 2. Verify RAG index exists:
ls assistant/rag_index.json

# 3. Re-index if missing:
cd assistant
python3 simple_rag.py index

# 4. Check sample tasks loaded:
curl http://localhost:5001/api/tasks/query
```

## 📚 Next Steps

1. **Read full documentation:** `project/docs/TEAM_ASSISTANT.md`
2. **Customize the UI:** Edit `AssistantChatScreen.kt`
3. **Add persistence:** Replace in-memory tasks with database
4. **Extend intents:** Add custom query patterns
5. **Deploy backend:** Use production WSGI server

## 🎨 Customization Ideas

### 1. Add to Navigation Drawer

```kotlin
// In your navigation setup:
NavHost(navController, startDestination = "home") {
    composable("assistant") {
        AssistantChatScreen(viewModel, onNavigateBack = {
            navController.popBackStack()
        })
    }
}

// Add menu item:
NavigationDrawerItem(
    icon = { Icon(Icons.Default.Assistant, null) },
    label = { Text("Team Assistant") },
    selected = false,
    onClick = { navController.navigate("assistant") }
)
```

### 2. Add Floating Action Button

```kotlin
FloatingActionButton(
    onClick = {
        val intent = Intent(context, AssistantChatActivity::class.java)
        context.startActivity(intent)
    }
) {
    Icon(Icons.Default.Chat, "Open Assistant")
}
```

### 3. Add Quick Actions

```kotlin
// In your main screen:
Row(
    horizontalArrangement = Arrangement.spacedBy(8.dp)
) {
    AssistChip(
        onClick = { openAssistantWithQuery("Show high priority tasks") },
        label = { Text("📋 Tasks") }
    )
    AssistChip(
        onClick = { openAssistantWithQuery("Project status") },
        label = { Text("📊 Status") }
    )
}

fun openAssistantWithQuery(query: String) {
    val intent = Intent(context, AssistantChatActivity::class.java)
    intent.putExtra("initial_query", query)
    context.startActivity(intent)
}
```

## 💬 Support

- 📖 Full docs: `project/docs/TEAM_ASSISTANT.md`
- 🐛 Issues: Check troubleshooting section
- 🧪 Test: Run `./test_team_assistant.sh`

## ✅ Success Checklist

- [ ] Backend starts without errors
- [ ] Health check returns `{"status":"healthy"}`
- [ ] RAG index exists: `ls assistant/rag_index.json`
- [ ] Sample tasks loaded (5 tasks)
- [ ] Android app builds successfully
- [ ] Can open AssistantChatActivity
- [ ] Chat UI appears with welcome message
- [ ] Can send messages and receive responses
- [ ] Quick actions work
- [ ] Task queries return results
- [ ] Documentation search works

---

**Ready to go!** 🎉

Try your first query: "Show high priority tasks"
