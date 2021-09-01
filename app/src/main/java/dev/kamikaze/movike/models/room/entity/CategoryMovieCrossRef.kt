package dev.kamikaze.movike.models.room.entity

import androidx.room.Entity

@Entity(primaryKeys = ["categoryId", "id"])
data class CategoryMovieCrossRef(var categoryId: Int, var id: Int)
