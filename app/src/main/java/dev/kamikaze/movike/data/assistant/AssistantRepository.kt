package dev.kamikaze.movike.data.assistant

import dev.kamikaze.movike.models.assistant.*
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Repository for assistant-related operations
 * Combines RAG, MCP (Git & CRM), and task management
 */
@Singleton
class AssistantRepository @Inject constructor(
    private val apiService: AssistantApiService
) {

    /**
     * Ask the assistant a question with full context
     */
    suspend fun askQuestion(
        question: String,
        includeRAG: Boolean = true,
        includeGitContext: Boolean = true,
        includeTasks: Boolean = true
    ): Result<AssistantResponse> {
        val context = AssistantContext(
            includeRAG = includeRAG,
            includeGitContext = includeGitContext,
            includeTasks = includeTasks
        )
        val request = AssistantRequest(question, context)
        return apiService.askQuestion(request)
    }

    /**
     * Get project status summary
     */
    suspend fun getProjectStatus(): Result<ProjectStatus> {
        return apiService.getProjectStatus()
    }

    /**
     * Query tasks with filters
     */
    suspend fun queryTasks(
        priority: TaskPriority? = null,
        status: TaskStatus? = null,
        assignee: String? = null,
        tags: List<String>? = null,
        limit: Int = 10
    ): Result<List<Task>> {
        val query = TaskQuery(
            priority = priority,
            status = status,
            assignee = assignee,
            tags = tags,
            limit = limit
        )
        return apiService.queryTasks(query)
    }

    /**
     * Get high priority tasks
     */
    suspend fun getHighPriorityTasks(): Result<List<Task>> {
        return queryTasks(priority = TaskPriority.HIGH)
    }

    /**
     * Create a new task
     */
    suspend fun createTask(
        title: String,
        description: String,
        priority: TaskPriority = TaskPriority.MEDIUM,
        assignee: String? = null,
        dueDate: Long? = null,
        tags: List<String> = emptyList()
    ): Result<Task> {
        val request = CreateTaskRequest(
            title = title,
            description = description,
            priority = priority,
            assignee = assignee,
            dueDate = dueDate,
            tags = tags
        )
        return apiService.createTask(request)
    }

    /**
     * Get task recommendations
     */
    suspend fun getTaskRecommendations(): Result<List<String>> {
        return apiService.getTaskRecommendations()
    }

    /**
     * Search documentation using RAG
     */
    suspend fun searchDocumentation(query: String, limit: Int = 5): Result<List<DocumentSource>> {
        return apiService.searchDocumentation(query, limit)
    }

    /**
     * Get Git context
     */
    suspend fun getGitContext(): Result<GitContext> {
        return apiService.getGitContext()
    }

    /**
     * Get comprehensive answer with all context
     * This is the main method that combines everything
     */
    fun getComprehensiveAnswer(question: String): Flow<ChatMessage> = flow {
        // Emit loading message
        emit(ChatMessage(
            content = "Analyzing your question...",
            role = MessageRole.ASSISTANT,
            isLoading = true
        ))

        // Parse question for intent
        val intent = parseIntent(question)

        when (intent) {
            QueryIntent.TASK_QUERY -> handleTaskQuery(question)
            QueryIntent.TASK_CREATE -> handleTaskCreate(question)
            QueryIntent.PROJECT_STATUS -> handleProjectStatus()
            QueryIntent.DOCUMENTATION -> handleDocumentation(question)
            QueryIntent.GIT_CONTEXT -> handleGitContext()
            QueryIntent.GENERAL -> handleGeneralQuery(question)
        }.fold(
            onSuccess = { message -> emit(message) },
            onFailure = { error ->
                emit(ChatMessage(
                    content = "Sorry, I encountered an error: ${error.message}",
                    role = MessageRole.ASSISTANT,
                    error = error.message
                ))
            }
        )
    }

    /**
     * Parse user intent from question
     */
    private fun parseIntent(question: String): QueryIntent {
        val lowerQuestion = question.lowercase()
        return when {
            // Check for task creation patterns first (more specific)
            lowerQuestion.contains("create task") ||
            lowerQuestion.contains("create task:") ||
            lowerQuestion.contains("add task") ||
            lowerQuestion.contains("add task:") ||
            lowerQuestion.contains("new task") ||
            lowerQuestion.contains("new task:") ||
            lowerQuestion.contains("создать задач") ||
            lowerQuestion.contains("создай задач") ||
            lowerQuestion.contains("добавить задач") -> QueryIntent.TASK_CREATE

            lowerQuestion.contains("задач") ||
            lowerQuestion.contains("task") ||
            lowerQuestion.contains("приоритет") ||
            lowerQuestion.contains("priority") -> QueryIntent.TASK_QUERY

            lowerQuestion.contains("статус проекта") ||
            lowerQuestion.contains("project status") ||
            lowerQuestion.contains("что делать") ||
            lowerQuestion.contains("what to do") -> QueryIntent.PROJECT_STATUS

            lowerQuestion.contains("документац") ||
            lowerQuestion.contains("documentation") ||
            lowerQuestion.contains("как работает") ||
            lowerQuestion.contains("how does") -> QueryIntent.DOCUMENTATION

            lowerQuestion.contains("git") ||
            lowerQuestion.contains("branch") ||
            lowerQuestion.contains("commit") -> QueryIntent.GIT_CONTEXT

            else -> QueryIntent.GENERAL
        }
    }

    private suspend fun handleTaskQuery(question: String): Result<ChatMessage> {
        // Extract priority from question if present
        val priority = when {
            question.lowercase().contains("high") || question.lowercase().contains("высок") -> TaskPriority.HIGH
            question.lowercase().contains("critical") || question.lowercase().contains("критич") -> TaskPriority.CRITICAL
            else -> null
        }

        return queryTasks(priority = priority).map { tasks ->
            val recommendations = getTaskRecommendations().getOrNull() ?: emptyList()

            val content = buildString {
                appendLine("Found ${tasks.size} tasks:")
                tasks.forEachIndexed { index, task ->
                    appendLine("\n${index + 1}. [${task.priority}] ${task.title}")
                    appendLine("   Status: ${task.status}")
                    appendLine("   ${task.description}")
                }

                if (recommendations.isNotEmpty()) {
                    appendLine("\n📋 Recommendations:")
                    recommendations.forEach { rec ->
                        appendLine("• $rec")
                    }
                }
            }

            ChatMessage(
                content = content,
                role = MessageRole.ASSISTANT,
                metadata = MessageMetadata(relatedTasks = tasks, suggestions = recommendations)
            )
        }
    }

    private suspend fun handleTaskCreate(question: String): Result<ChatMessage> {
        // The server will parse the task details from the question text
        // and create the task automatically via the /api/assistant/ask endpoint
        return askQuestion(
            question = question,
            includeRAG = false,  // Don't need RAG for task creation
            includeGitContext = false,  // Don't need git context
            includeTasks = false  // Don't need existing tasks
        ).map { response ->
            ChatMessage(
                content = response.answer,
                role = MessageRole.ASSISTANT,
                metadata = MessageMetadata(
                    relatedTasks = response.relatedTasks,
                    suggestions = response.suggestions
                )
            )
        }
    }

    private suspend fun handleProjectStatus(): Result<ChatMessage> {
        return getProjectStatus().map { status ->
            val content = buildString {
                appendLine("📊 Project Status:")
                appendLine("Total tasks: ${status.totalTasks}")
                appendLine("\nBy Priority:")
                status.tasksByPriority.forEach { (priority, count) ->
                    appendLine("  $priority: $count")
                }
                appendLine("\nBy Status:")
                status.tasksByStatus.forEach { (taskStatus, count) ->
                    appendLine("  $taskStatus: $count")
                }

                if (status.highPriorityTasks.isNotEmpty()) {
                    appendLine("\n🔥 High Priority Tasks:")
                    status.highPriorityTasks.take(3).forEach { task ->
                        appendLine("  • ${task.title}")
                    }
                }

                if (status.recommendations.isNotEmpty()) {
                    appendLine("\n💡 Recommendations:")
                    status.recommendations.forEach { rec ->
                        appendLine("  • $rec")
                    }
                }
            }

            ChatMessage(
                content = content,
                role = MessageRole.ASSISTANT,
                metadata = MessageMetadata(
                    relatedTasks = status.highPriorityTasks,
                    suggestions = status.recommendations
                )
            )
        }
    }

    private suspend fun handleDocumentation(question: String): Result<ChatMessage> {
        return searchDocumentation(question).map { sources ->
            val content = buildString {
                appendLine("📚 Found ${sources.size} relevant documentation sections:")
                sources.forEachIndexed { index, source ->
                    appendLine("\n${index + 1}. From ${source.file}:")
                    appendLine(source.content.take(200) + "...")
                }
            }

            ChatMessage(
                content = content,
                role = MessageRole.ASSISTANT,
                metadata = MessageMetadata(sources = sources)
            )
        }
    }

    private suspend fun handleGitContext(): Result<ChatMessage> {
        return getGitContext().map { gitContext ->
            val content = buildString {
                appendLine("🔀 Git Context:")
                appendLine("Current branch: ${gitContext.currentBranch}")

                if (gitContext.modifiedFiles.isNotEmpty()) {
                    appendLine("\nModified files:")
                    gitContext.modifiedFiles.take(5).forEach { file ->
                        appendLine("  • $file")
                    }
                }

                if (gitContext.recentCommits.isNotEmpty()) {
                    appendLine("\nRecent commits:")
                    gitContext.recentCommits.take(3).forEach { commit ->
                        appendLine("  • $commit")
                    }
                }

                gitContext.status?.let { status ->
                    appendLine("\nStatus: $status")
                }
            }

            ChatMessage(
                content = content,
                role = MessageRole.ASSISTANT
            )
        }
    }

    private suspend fun handleGeneralQuery(question: String): Result<ChatMessage> {
        return askQuestion(question).map { response ->
            ChatMessage(
                content = response.answer,
                role = MessageRole.ASSISTANT,
                metadata = MessageMetadata(
                    sources = response.sources,
                    relatedTasks = response.relatedTasks,
                    suggestions = response.suggestions
                )
            )
        }
    }

    private enum class QueryIntent {
        TASK_QUERY,
        TASK_CREATE,
        PROJECT_STATUS,
        DOCUMENTATION,
        GIT_CONTEXT,
        GENERAL
    }
}
