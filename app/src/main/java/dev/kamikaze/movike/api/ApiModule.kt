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
import javax.inject.Singleton

@Module
class ApiModule {

    @Provides
    @Singleton
    fun provideLogInterceptor(): HttpLoggingInterceptor {
        return HttpLoggingInterceptor().setLevel(HttpLoggingInterceptor.Level.BODY)
    }

    @Provides
    @Singleton
    fun provideAuthInterceptor(@ApiQualifier api: String): Interceptor {
        return Interceptor { chain ->
            val newUrl = chain.request().url
                .newBuilder()
                .addQueryParameter("api_key", api)
                .build()
            val authorizationRequest = chain.request()
                .newBuilder()
                .url(newUrl)
                .build()
            chain.proceed(authorizationRequest)
        }
    }

    @Provides
    @Singleton
    fun provideHttpClient(
        @NotNull authInterceptor: Interceptor,
        @NotNull logInterceptor: HttpLoggingInterceptor
    ): OkHttpClient {
        return OkHttpClient()
            .newBuilder()
            .addInterceptor(authInterceptor)
            .addInterceptor(logInterceptor)
            .build()
    }

    @Provides
    @Singleton
    @ExperimentalSerializationApi
    fun provideRetrofit(
        @NonNull okHttpClient: OkHttpClient
    ): Retrofit {
        val contentType = "application/json".toMediaType()
        val jsonConverter = Json {
            ignoreUnknownKeys = true
        }
        return Retrofit.Builder()
            .client(okHttpClient)
            .baseUrl(BuildConfig.BASE_URL)
            .addConverterFactory(jsonConverter.asConverterFactory(contentType))
            .build()
    }

    @Provides
    @Singleton
    fun provideMainService(@NonNull retrofit: Retrofit): ApiService {
        return retrofit.create(ApiService::class.java)
    }

}