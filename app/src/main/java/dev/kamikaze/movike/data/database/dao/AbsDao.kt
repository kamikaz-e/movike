package dev.kamikaze.movike.data.database.dao

import androidx.room.Delete
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Update

interface AbsDao<Entity> {

    @Delete
    fun deleteAll()

    @Update(onConflict = OnConflictStrategy.REPLACE)
    fun update(item: Entity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insert(item: Entity)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    fun insert(items: List<Entity>)

    @Delete
    fun delete(item: Entity)

    fun getListById(id: Int): List<Entity>

    fun isExistById(id: Int) = getListById(id).isNotEmpty()


}
