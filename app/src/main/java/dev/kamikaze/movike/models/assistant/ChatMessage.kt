package dev.kamikaze.movike.models.assistant

import kotlinx.serialization.Serializable
import java.util.UUID

/**
 * Represents a single message in the chat
 */
@Serializable
data class ChatMessage(
    val id: String = UUID.randomUUID().toString(),
    val content: String,
    val role: MessageRole,
    val timestamp: Long = System.currentTimeMillis(),
    val isLoading: Boolean = false,
    val error: String? = null,
    val metadata: MessageMetadata? = null
)

/**
 * Role of the message sender
 */
@Serializable
enum class MessageRole {
    USER,
    ASSISTANT,
    SYSTEM
}

/**
 * Additional metadata for messages
 */
@Serializable
data class MessageMetadata(
    val sources: List<DocumentSource>? = null,
    val relatedTasks: List<Task>? = null,
    val suggestions: List<String>? = null
)

/**
 * Document source from RAG system
 */
@Serializable
data class DocumentSource(
    val file: String,
    val content: String,
    val score: Double
)
