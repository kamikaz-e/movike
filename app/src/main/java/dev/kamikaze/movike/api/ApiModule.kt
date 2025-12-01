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
        interceptor.level = if (BuildConfig.DEBUG) {
            HttpLoggingInterceptor.Level.BODY
        } else {
            HttpLoggingInterceptor.Level.NONE
        }
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
            
            // Log URL for debugging
            if (BuildConfig.DEBUG) {
                android.util.Log.d("ApiModule", "Request URL: ${originalUrl}")
                android.util.Log.d("ApiModule", "API Key configured: ${api.take(4)}...")
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
                
                // Log response status for debugging
                if (BuildConfig.DEBUG) {
                    android.util.Log.d("ApiModule", "Response status: ${response.code}")
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
                .build()
    }
    
    @Provides
    @Singleton
    @ExperimentalSerializationApi
    fun provideRetrofit(okHttpClient: OkHttpClient): Retrofit {
        val baseUrl = BuildConfig.BASE_URL
        if (baseUrl.isBlank()) {
            throw IllegalStateException("BASE_URL is not configured in BuildConfig")
        }
        val contentType = "application/json".toMediaType()
        val jsonConverter = Json {
            ignoreUnknownKeys = true
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