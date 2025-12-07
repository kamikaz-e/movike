package dev.kamikaze.movike.data.assistant

import android.util.Log
import dev.kamikaze.movike.BuildConfig
import dev.kamikaze.movike.models.assistant.*
import io.ktor.client.*
import io.ktor.client.call.*
import io.ktor.client.plugins.*
import io.ktor.client.request.*
import io.ktor.http.*
import kotlinx.serialization.json.Json
import javax.inject.Inject
import javax.inject.Singleton

/**
 * Custom exception for HTTP errors in Assistant API
 */
class AssistantHttpException(
    val statusCode: HttpStatusCode,
    message: String
) : Exception(message)

/**
 * API service for communicating with the Python assistant backend
 */
@Singleton
class AssistantApiService @Inject constructor(
    private val httpClient: HttpClient,
    private val baseUrl: String
) {

    /**
     * Ask the assistant a question
     */
    suspend fun askQuestion(request: AssistantRequest): Result<AssistantResponse> {
        return try {
            val response = httpClient.post("$baseUrl/api/assistant/ask") {
                contentType(ContentType.Application.Json)
                setBody(request)
            }
            
            val statusCode = response.status.value
            if (statusCode in 200..299) {
                Result.success(response.body())
            } else {
                val errorMessage = "HTTP ${response.status.value}: ${response.status.description}"
                if (BuildConfig.DEBUG) {
                    Log.e("AssistantApiService", "askQuestion failed: $errorMessage")
                }
                Result.failure(AssistantHttpException(response.status, errorMessage))
            }
        } catch (e: ClientRequestException) {
            if (BuildConfig.DEBUG) {
                Log.e("AssistantApiService", "askQuestion ClientRequestException: ${e.message}", e)
            }
            Result.failure(e)
        } catch (e: Exception) {
            if (BuildConfig.DEBUG) {
                Log.e("AssistantApiService", "askQuestion Exception: ${e.message}", e)
            }
            Result.failure(e)
        }
    }

    /**
     * Get project status with task statistics
     */
    suspend fun getProjectStatus(): Result<ProjectStatus> {
        return try {
            val response = httpClient.get("$baseUrl/api/assistant/status")
            Result.success(response.body())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Query tasks with filters
     */
    suspend fun queryTasks(query: TaskQuery): Result<List<Task>> {
        return try {
            val response = httpClient.post("$baseUrl/api/tasks/query") {
                contentType(ContentType.Application.Json)
                setBody(query)
            }
            
            // Check HTTP status code
            val statusCode = response.status.value
            if (statusCode in 200..299) {
                Result.success(response.body())
            } else {
                val errorMessage = "HTTP ${response.status.value}: ${response.status.description}"
                if (BuildConfig.DEBUG) {
                    Log.e("AssistantApiService", "queryTasks failed: $errorMessage")
                    Log.e("AssistantApiService", "Request URL: $baseUrl/api/tasks/query")
                    Log.e("AssistantApiService", "Request body: ${query}")
                }
                Result.failure(AssistantHttpException(response.status, errorMessage))
            }
        } catch (e: ClientRequestException) {
            val errorMessage = "Request failed: ${e.response.status.value} - ${e.message}"
            if (BuildConfig.DEBUG) {
                Log.e("AssistantApiService", "queryTasks ClientRequestException: $errorMessage", e)
                try {
                    val responseBody = e.response.body<String>()
                    Log.e("AssistantApiService", "Response body: $responseBody")
                } catch (ex: Exception) {
                    Log.e("AssistantApiService", "Could not read response body: ${ex.message}")
                }
            }
            Result.failure(e)
        } catch (e: ServerResponseException) {
            val errorMessage = "Server error: ${e.response.status.value} - ${e.message}"
            if (BuildConfig.DEBUG) {
                Log.e("AssistantApiService", "queryTasks ServerResponseException: $errorMessage", e)
            }
            Result.failure(e)
        } catch (e: Exception) {
            val errorMessage = "Network error: ${e.message}"
            if (BuildConfig.DEBUG) {
                Log.e("AssistantApiService", "queryTasks Exception: $errorMessage", e)
            }
            Result.failure(e)
        }
    }

    /**
     * Create a new task
     */
    suspend fun createTask(request: CreateTaskRequest): Result<Task> {
        return try {
            val response = httpClient.post("$baseUrl/api/tasks/create") {
                contentType(ContentType.Application.Json)
                setBody(request)
            }
            
            val statusCode = response.status.value
            if (statusCode in 200..299) {
                Result.success(response.body())
            } else {
                val errorMessage = "HTTP ${response.status.value}: ${response.status.description}"
                if (BuildConfig.DEBUG) {
                    Log.e("AssistantApiService", "createTask failed: $errorMessage")
                }
                Result.failure(AssistantHttpException(response.status, errorMessage))
            }
        } catch (e: ClientRequestException) {
            if (BuildConfig.DEBUG) {
                Log.e("AssistantApiService", "createTask ClientRequestException: ${e.message}", e)
            }
            Result.failure(e)
        } catch (e: Exception) {
            if (BuildConfig.DEBUG) {
                Log.e("AssistantApiService", "createTask Exception: ${e.message}", e)
            }
            Result.failure(e)
        }
    }

    /**
     * Get task recommendations based on priorities
     */
    suspend fun getTaskRecommendations(): Result<List<String>> {
        return try {
            val response = httpClient.get("$baseUrl/api/assistant/recommendations")
            Result.success(response.body())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Search documentation using RAG
     */
    suspend fun searchDocumentation(query: String, limit: Int = 5): Result<List<DocumentSource>> {
        return try {
            val response = httpClient.get("$baseUrl/api/rag/search") {
                parameter("query", query)
                parameter("limit", limit)
            }
            Result.success(response.body())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    /**
     * Get Git context information
     */
    suspend fun getGitContext(): Result<GitContext> {
        return try {
            val response = httpClient.get("$baseUrl/api/git/context")
            Result.success(response.body())
        } catch (e: Exception) {
            Result.failure(e)
        }
    }
}
