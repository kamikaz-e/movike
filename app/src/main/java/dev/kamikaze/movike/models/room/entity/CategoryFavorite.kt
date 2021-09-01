package dev.kamikaze.movike.models.room.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import kotlinx.serialization.Serializable

@Entity(tableName = "category")
@Serializable
data class CategoryFavorite(
    @PrimaryKey(autoGenerate = true)
    var categoryId: Int = 0,
    var categoryTitle: String = ""
)
