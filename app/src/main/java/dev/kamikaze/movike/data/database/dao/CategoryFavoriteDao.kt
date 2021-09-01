package dev.kamikaze.movike.data.database.dao

import androidx.room.Dao
import androidx.room.Query
import androidx.room.Transaction
import dev.kamikaze.movike.models.room.entity.CategoryFavorite
import dev.kamikaze.movike.models.room.relate.CategoryWithMovies

@Dao
interface CategoryFavoriteDao : AbsDao<CategoryFavorite> {

    @Query("SELECT * FROM CATEGORY where categoryId LIKE :id")
    override fun getListById(id: Int): List<CategoryFavorite>

    @Query("DELETE FROM CATEGORY")
    override fun deleteAll()

    @Transaction
    @Query("SELECT * FROM CATEGORY")
    fun getList(): List<CategoryWithMovies>

    fun getById(id: Int) = getListById(id).firstOrNull()

}
