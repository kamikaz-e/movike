package dev.kamikaze.movike.di.modules

import dagger.Module
import dagger.Provides
import dev.kamikaze.movike.api.ApiService
import dev.kamikaze.movike.data.database.DatabaseImpl
import dev.kamikaze.movike.domain.usecases.*
import dev.kamikaze.movike.repository.RepositoryImpl
import javax.inject.Singleton

@Module
class DataModule {

    @Singleton
    @Provides
    fun providesMainRepository(apiService: ApiService, database: DatabaseImpl) = RepositoryImpl(apiService, database)

    @Provides
    fun provideSaveMovieAsWatchUseCase(repository: RepositoryImpl) = SaveMovieAsWatchUseCase(repository)

    @Provides
    fun provideCheckMovieAsWatchUseCase(repository: RepositoryImpl) = CheckMovieAsWatchUseCase(repository)

    @Provides
    fun provideGetMoviesWithCategoryUseCase(repository: RepositoryImpl) = GetMoviesWithCategoryUseCase(repository)

    @Provides
    fun provideGetCategoriesFavoriteUseCase(repository: RepositoryImpl) = GetCategoriesFavoriteUseCase(repository)

    @Provides
    fun provideInitStartValueUseCase(repository: RepositoryImpl) = InitStartValueUseCase(repository)

}