package dev.kamikaze.movike.models.room.relate

import androidx.room.Embedded
import androidx.room.Junction
import androidx.room.Relation
import dev.kamikaze.movike.models.room.entity.CategoryFavorite
import dev.kamikaze.movike.models.room.entity.CategoryMovieCrossRef
import dev.kamikaze.movike.models.room.entity.Movie

data class MovieWithCategories(

    @Embedded val movie: Movie,

    @Relation(
        parentColumn = "id",
        entityColumn = "categoryId",
        associateBy = Junction(CategoryMovieCrossRef::class)
    )
    val categoryList: List<CategoryFavorite>

)
