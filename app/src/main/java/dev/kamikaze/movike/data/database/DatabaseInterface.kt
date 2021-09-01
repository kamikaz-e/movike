package dev.kamikaze.movike.data.database

import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.models.room.relate.CategoryWithMovies
import dev.kamikaze.movike.models.room.relate.MovieWithCategories

interface DatabaseInterface {

    val moviesWithCategory: List<MovieWithCategories>

    val categoriesFavorite: List<CategoryWithMovies>

    fun saveMovieAsWatch(movie: Movie): Boolean

    fun isWatchMovieCheck(movie: Movie): Boolean

    fun initStartValue()

}