package dev.kamikaze.movike.models.assistant

import kotlinx.serialization.Serializable

/**
 * Request to ask the assistant a question
 */
@Serializable
data class AssistantRequest(
    val question: String,
    val context: AssistantContext? = null
)

/**
 * Context for assistant queries
 */
@Serializable
data class AssistantContext(
    val includeRAG: Boolean = true,
    val includeGitContext: Boolean = true,
    val includeTasks: Boolean = true,
    val maxResults: Int = 5
)

/**
 * Response from the assistant
 */
@Serializable
data class AssistantResponse(
    val answer: String,
    val sources: List<DocumentSource> = emptyList(),
    val relatedTasks: List<Task> = emptyList(),
    val suggestions: List<String> = emptyList(),
    val gitContext: GitContext? = null
)

/**
 * Git context information
 */
@Serializable
data class GitContext(
    val currentBranch: String,
    val recentCommits: List<String> = emptyList(),
    val modifiedFiles: List<String> = emptyList(),
    val status: String? = null
)

/**
 * Project status summary
 */
@Serializable
data class ProjectStatus(
    val totalTasks: Int,
    val tasksByPriority: Map<String, Int>,
    val tasksByStatus: Map<String, Int>,
    val highPriorityTasks: List<Task>,
    val blockedTasks: List<Task>,
    val recommendations: List<String>
)
