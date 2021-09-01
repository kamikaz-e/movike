package dev.kamikaze.movike.data.database

import androidx.room.Database
import androidx.room.RoomDatabase
import dev.kamikaze.movike.data.database.dao.CategoryFavoriteDao
import dev.kamikaze.movike.data.database.dao.CategoryMovieCrossRefDao
import dev.kamikaze.movike.data.database.dao.MovieDao
import dev.kamikaze.movike.models.room.entity.CategoryFavorite
import dev.kamikaze.movike.models.room.entity.CategoryMovieCrossRef
import dev.kamikaze.movike.models.room.entity.Movie

@Database(
    entities = [Movie::class, CategoryFavorite::class, CategoryMovieCrossRef::class],
    version = 1,
)
abstract class AppDatabase : RoomDatabase() {

    abstract fun movieDao(): MovieDao

    abstract fun categoryFavoriteDao(): CategoryFavoriteDao

    abstract fun crossRefCategoryMovieDao(): CategoryMovieCrossRefDao

}