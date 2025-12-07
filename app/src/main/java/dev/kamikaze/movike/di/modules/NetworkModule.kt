package dev.kamikaze.movike.di.modules

import dagger.Module
import dagger.Provides
import dev.kamikaze.movike.BuildConfig
import io.ktor.client.*
import io.ktor.client.engine.android.*
import io.ktor.client.plugins.*
import io.ktor.client.plugins.contentnegotiation.*
import io.ktor.client.plugins.logging.*
import io.ktor.serialization.kotlinx.json.*
import kotlinx.serialization.json.Json
import javax.inject.Singleton

@Module
class NetworkModule {

    @Provides
    @Singleton
    fun provideJson(): Json = Json {
        ignoreUnknownKeys = true
        isLenient = true
        encodeDefaults = true
        prettyPrint = true
    }

    @Provides
    @Singleton
    fun provideHttpClient(json: Json): HttpClient {
        return HttpClient(Android) {
            // JSON serialization
            install(ContentNegotiation) {
                json(json)
            }

            // Logging
            install(Logging) {
                logger = Logger.ANDROID
                level = LogLevel.BODY
            }

            // Timeout configuration
            install(HttpTimeout) {
                requestTimeoutMillis = 30000
                connectTimeoutMillis = 30000
                socketTimeoutMillis = 30000
            }

            // Default headers
            defaultRequest {
                headers.append("Accept", "application/json")
            }
        }
    }

    @Provides
    @Singleton
    fun provideAssistantBaseUrl(): String {
        // Use BuildConfig value which is configured for emulator (10.0.2.2) or real device (IP address)
        // For Android Emulator: 10.0.2.2 maps to host machine's localhost
        // For real device: use your computer's IP address (e.g., "http://192.168.1.100:5001")
        return BuildConfig.ASSISTANT_BASE_URL
    }
}
