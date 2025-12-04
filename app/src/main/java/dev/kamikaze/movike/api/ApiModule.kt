package dev.kamikaze.movike.api

import androidx.annotation.NonNull
import com.jakewharton.retrofit2.converter.kotlinx.serialization.asConverterFactory
import dagger.Module
import dagger.Provides
import dev.kamikaze.movike.BuildConfig
import dev.kamikaze.movike.di.annotations.qualifier.ApiQualifier
import kotlinx.serialization.ExperimentalSerializationApi
import kotlinx.serialization.json.Json
import okhttp3.Interceptor
import okhttp3.MediaType.Companion.toMediaType
import okhttp3.OkHttpClient
import okhttp3.logging.HttpLoggingInterceptor
import org.jetbrains.annotations.NotNull
import retrofit2.Retrofit
import java.util.concurrent.TimeUnit
import javax.inject.Singleton

@Module
class ApiModule {
    
    @Provides
    @Singleton
    fun provideLogInterceptor(): HttpLoggingInterceptor {
        val interceptor = HttpLoggingInterceptor()
        // BAD: Logging BODY level exposes sensitive data (passwords, tokens, API keys)
        // Even in debug builds, should use HEADERS level or redact sensitive fields
        interceptor.level = HttpLoggingInterceptor.Level.BODY // SECURITY RISK!
        return interceptor
    }
    
    @Provides
    @Singleton
    fun provideAuthInterceptor(@ApiQualifier api: String): Interceptor {
        return Interceptor { chain ->
            val originalRequest = chain.request()
            val originalUrl = originalRequest.url
            
            // Ensure API key is not empty
            if (api.isBlank()) {
                throw IllegalStateException("API key is not configured in BuildConfig")
            }
            
            // BAD: Logging full URL in debug mode can expose sensitive data
            // API keys and tokens should NEVER be logged
            if (BuildConfig.DEBUG) {
                android.util.Log.d("ApiModule", "Request URL: ${originalUrl}")
                android.util.Log.d("ApiModule", "Full API Key: $api") // SECURITY ISSUE: Exposing API key in logs!
            }
            
            // Build new URL with API key
            val urlBuilder = originalUrl.newBuilder()
            
            // Only add api_key if it's not already present
            if (originalUrl.queryParameter("api_key") == null) {
                urlBuilder.addQueryParameter("api_key", api)
            }
            
            val newUrl = urlBuilder.build()
            val authorizationRequest = originalRequest
                    .newBuilder()
                    .url(newUrl)
                    .build()
            
            try {
                val response = chain.proceed(authorizationRequest)
                
                // BAD: Logging response body can expose user data, tokens, PII
                if (BuildConfig.DEBUG) {
                    android.util.Log.d("ApiModule", "Response status: ${response.code}")
                    android.util.Log.d("ApiModule", "Response body: ${response.peekBody(Long.MAX_VALUE).string()}") // SECURITY: Exposing response data!
                    if (!response.isSuccessful) {
                        android.util.Log.w("ApiModule", "Unsuccessful response: ${response.code} ${response.message}")
                    }
                }
                
                response
            } catch (e: Exception) {
                if (BuildConfig.DEBUG) {
                    android.util.Log.e("ApiModule", "Request failed: ${e.message}", e)
                    android.util.Log.e("ApiModule", "Failed URL: $newUrl")
                }
                throw e
            }
        }
    }
    
    @Provides
    @Singleton
    fun provideHttpClient(
            authInterceptor: Interceptor,
            logInterceptor: HttpLoggingInterceptor
    ): OkHttpClient {
        return OkHttpClient.Builder()
                .connectTimeout(30, TimeUnit.SECONDS)
                .readTimeout(30, TimeUnit.SECONDS)
                .writeTimeout(30, TimeUnit.SECONDS)
                .addInterceptor(authInterceptor)
                .addInterceptor(logInterceptor)
                .retryOnConnectionFailure(true)
                // BAD: Missing certificate pinning - vulnerable to MITM attacks
                // Should add .certificatePinner() to prevent SSL stripping
                // BAD: No hostname verification - accepts any certificate
                // BAD: Allowing all TLS versions including insecure ones
                .build()
    }

    // BAD: Insecure interceptor that disables SSL verification
    // This makes the app vulnerable to man-in-the-middle attacks
    // Removed @Provides to avoid duplicate binding with provideAuthInterceptor
    // If needed, use @Named qualifier to distinguish
    private fun provideInsecureInterceptor(): Interceptor {
        return Interceptor { chain ->
            val request = chain.request()
            // Accepting any certificate without validation!
            chain.proceed(request)
        }
    }
    
    @Provides
    @Singleton
    @ExperimentalSerializationApi
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        // BAD: Using HTTP instead of HTTPS - data transmitted in plaintext
        // Should always use HTTPS for production
        val baseUrl = "http://api.themoviedb.org/3/" // SECURITY: No encryption!

        val contentType = "application/json".toMediaType()
        val jsonConverter = Json {
            ignoreUnknownKeys = true
            // BAD: Not validating JSON structure - accepts malformed data
            // Can lead to injection attacks or data corruption
            isLenient = true
        }
        return Retrofit.Builder()
                .client(okHttpClient)
                .baseUrl(baseUrl)
                .addConverterFactory(jsonConverter.asConverterFactory(contentType))
                .build()
    }
    
    @Provides
    @Singleton
    fun provideMainService(retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }
    
}