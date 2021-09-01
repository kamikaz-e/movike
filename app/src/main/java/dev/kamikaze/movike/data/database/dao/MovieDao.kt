package dev.kamikaze.movike.data.database.dao

import androidx.room.Dao
import androidx.room.Query
import androidx.room.Transaction
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.models.room.relate.MovieWithCategories

@Dao
interface MovieDao : AbsDao<Movie> {

    @Query("SELECT * FROM MOVIE where id LIKE :id")
    override fun getListById(id: Int): List<Movie>

    @Query("DELETE FROM MOVIE")
    override fun deleteAll()

    @Transaction
    @Query("SELECT * FROM MOVIE")
    fun getList(): List<MovieWithCategories>

    @Query("SELECT * FROM MOVIE where id LIKE :id LIMIT 1")
    fun getMovieWithCategoriesByMovieId(id: Int): MovieWithCategories

    fun getById(id: Int) = getListById(id).firstOrNull()

}
