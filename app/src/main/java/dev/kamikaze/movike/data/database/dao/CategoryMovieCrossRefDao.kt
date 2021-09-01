package dev.kamikaze.movike.data.database.dao

import androidx.room.Dao
import androidx.room.Query
import dev.kamikaze.movike.models.room.entity.CategoryMovieCrossRef

@Dao
interface CategoryMovieCrossRefDao : AbsDao<CategoryMovieCrossRef> {

    @Query("SELECT * FROM CategoryMovieCrossRef where categoryId LIKE :id")
    override fun getListById(id: Int): List<CategoryMovieCrossRef>

    @Query("DELETE FROM CategoryMovieCrossRef")
    override fun deleteAll()

    @Query("SELECT * FROM CategoryMovieCrossRef")
    fun getList(): List<CategoryMovieCrossRef>

    @Query("SELECT * FROM CategoryMovieCrossRef where categoryId LIKE :categoryId and id LIKE :movieId LIMIT 1")
    fun getCrossRefMovieCategoryById(categoryId: Int, movieId: Int): CategoryMovieCrossRef?

    fun insert(categoryId: Int, movieId: Int) {
        insert(CategoryMovieCrossRef(categoryId, movieId))
    }

}
