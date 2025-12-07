package dev.kamikaze.movike.models.assistant

import kotlinx.serialization.Serializable

/**
 * Represents a project task
 */
@Serializable
data class Task(
    val id: String,
    val title: String,
    val description: String,
    val priority: TaskPriority,
    val status: TaskStatus,
    val assignee: String? = null,
    val createdAt: Long,
    val updatedAt: Long,
    val dueDate: Long? = null,
    val tags: List<String> = emptyList()
)

/**
 * Task priority levels
 */
@Serializable
enum class TaskPriority {
    LOW,
    MEDIUM,
    HIGH,
    CRITICAL;

    companion object {
        fun fromString(value: String): TaskPriority {
            return when (value.lowercase()) {
                "low" -> LOW
                "medium" -> MEDIUM
                "high" -> HIGH
                "critical" -> CRITICAL
                else -> MEDIUM
            }
        }
    }
}

/**
 * Task status
 */
@Serializable
enum class TaskStatus {
    TODO,
    IN_PROGRESS,
    IN_REVIEW,
    DONE,
    BLOCKED;

    companion object {
        fun fromString(value: String): TaskStatus {
            return when (value.lowercase().replace("_", "")) {
                "todo" -> TODO
                "inprogress" -> IN_PROGRESS
                "inreview" -> IN_REVIEW
                "done" -> DONE
                "blocked" -> BLOCKED
                else -> TODO
            }
        }
    }
}

/**
 * Request to create a new task
 */
@Serializable
data class CreateTaskRequest(
    val title: String,
    val description: String,
    val priority: TaskPriority = TaskPriority.MEDIUM,
    val assignee: String? = null,
    val dueDate: Long? = null,
    val tags: List<String> = emptyList()
)

/**
 * Task query filters
 */
@Serializable
data class TaskQuery(
    val priority: TaskPriority? = null,
    val status: TaskStatus? = null,
    val assignee: String? = null,
    val tags: List<String>? = null,
    val limit: Int = 10
)
