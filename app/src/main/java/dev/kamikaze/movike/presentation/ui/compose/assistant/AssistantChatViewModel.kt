package dev.kamikaze.movike.presentation.ui.compose.assistant

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import dev.kamikaze.movike.data.assistant.AssistantRepository
import dev.kamikaze.movike.models.assistant.ChatMessage
import dev.kamikaze.movike.models.assistant.MessageRole
import kotlinx.coroutines.flow.*
import kotlinx.coroutines.launch
import javax.inject.Inject

/**
 * UI State for the chat screen
 */
data class AssistantChatUiState(
    val messages: List<ChatMessage> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

/**
 * ViewModel for the Assistant Chat screen
 * Manages chat state and communicates with the repository
 */
class AssistantChatViewModel @Inject constructor(
    private val repository: AssistantRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(AssistantChatUiState())
    val uiState: StateFlow<AssistantChatUiState> = _uiState.asStateFlow()

    private val _messages = mutableListOf<ChatMessage>()

    init {
        // Add welcome message
        addMessage(
            ChatMessage(
                content = """
                    👋 Hello! I'm your team assistant.

                    I can help you with:
                    • 📋 Task management (create, query, prioritize)
                    • 📚 Search project documentation (RAG)
                    • 🔀 Git context and status (MCP)
                    • 📊 Project status and recommendations

                    Try asking:
                    • "Create task: Fix memory leak with high priority. Description: Images not released properly"
                    • "Show tasks with high priority"
                    • "What should I do first?"
                    • "Search documentation about architecture"
                    • "What's the project status?"
                """.trimIndent(),
                role = MessageRole.SYSTEM
            )
        )
    }

    /**
     * Send a message to the assistant
     */
    fun sendMessage(text: String) {
        if (text.isBlank()) return

        // Add user message
        val userMessage = ChatMessage(
            content = text,
            role = MessageRole.USER
        )
        addMessage(userMessage)

        // Set loading state
        _uiState.update { it.copy(isLoading = true, error = null) }

        // Get assistant response
        viewModelScope.launch {
            repository.getComprehensiveAnswer(text)
                .catch { error ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            error = error.message
                        )
                    }
                    addMessage(
                        ChatMessage(
                            content = "Sorry, I encountered an error: ${error.message}",
                            role = MessageRole.ASSISTANT,
                            error = error.message
                        )
                    )
                }
                .collect { message ->
                    if (message.isLoading) {
                        // Replace loading message or add if first
                        val lastMessage = _messages.lastOrNull()
                        if (lastMessage?.isLoading == true) {
                            _messages[_messages.lastIndex] = message
                        } else {
                            addMessage(message)
                        }
                    } else {
                        // Replace loading message with final response
                        val lastMessage = _messages.lastOrNull()
                        if (lastMessage?.isLoading == true) {
                            _messages[_messages.lastIndex] = message
                        } else {
                            addMessage(message)
                        }
                        _uiState.update { it.copy(isLoading = false) }
                    }
                    updateMessages()
                }
        }
    }

    /**
     * Send a predefined quick action
     */
    fun sendQuickAction(action: String) {
        sendMessage(action)
    }

    /**
     * Clear all messages except the welcome message
     */
    fun clearChat() {
        _messages.clear()
        _messages.add(
            ChatMessage(
                content = "Chat cleared. How can I help you?",
                role = MessageRole.SYSTEM
            )
        )
        updateMessages()
    }

    /**
     * Get high priority tasks
     */
    fun getHighPriorityTasks() {
        sendMessage("Show me high priority tasks")
    }

    /**
     * Get project status
     */
    fun getProjectStatus() {
        sendMessage("What's the project status?")
    }

    /**
     * Search documentation
     */
    fun searchDocumentation(query: String) {
        sendMessage("Search documentation: $query")
    }

    /**
     * Create a task (opens a dialog in the UI)
     */
    fun createTask(title: String, description: String, priority: String) {
        sendMessage("Create task: $title with priority $priority. Description: $description")
    }

    private fun addMessage(message: ChatMessage) {
        _messages.add(message)
        updateMessages()
    }

    private fun updateMessages() {
        _uiState.update { it.copy(messages = _messages.toList()) }
    }
}
