package dev.kamikaze.movike.di.modules

import android.app.Application
import androidx.room.Room
import dev.kamikaze.movike.data.database.AppDatabase
import dev.kamikaze.movike.data.database.dao.CategoryFavoriteDao
import dev.kamikaze.movike.data.database.dao.CategoryMovieCrossRefDao
import dev.kamikaze.movike.data.database.dao.MovieDao
import dagger.Module
import dagger.Provides
import javax.inject.Singleton

@Module
class DBModule {

    companion object {
        private const val DB_NAME = "movike.db"

        @Volatile
        private var instance: AppDatabase? = null
    }

    @Singleton
    @Provides
    fun provideDatabase(application: Application): AppDatabase {
        if (instance != null) {
            return instance as AppDatabase
        }
        synchronized(this) {
            instance = Room.databaseBuilder(
                application,
                AppDatabase::class.java,
                DB_NAME
            ).fallbackToDestructiveMigration().build()
            return instance as AppDatabase
        }
    }

    @Singleton
    @Provides
    fun provideMovieDao(appDatabase: AppDatabase): MovieDao {
        return appDatabase.movieDao()
    }

    @Singleton
    @Provides
    fun provideCategoryFavoriteDao(appDatabase: AppDatabase): CategoryFavoriteDao {
        return appDatabase.categoryFavoriteDao()
    }

    @Singleton
    @Provides
    fun provideCategoryMovieCrossRefDao(appDatabase: AppDatabase): CategoryMovieCrossRefDao {
        return appDatabase.crossRefCategoryMovieDao()
    }

}
