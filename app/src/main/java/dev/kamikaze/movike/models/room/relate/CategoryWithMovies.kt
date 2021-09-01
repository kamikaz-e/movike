package dev.kamikaze.movike.models.room.relate

import androidx.room.Embedded
import androidx.room.Junction
import androidx.room.Relation
import dev.kamikaze.movike.models.room.entity.CategoryFavorite
import dev.kamikaze.movike.models.room.entity.CategoryMovieCrossRef
import dev.kamikaze.movike.models.room.entity.Movie

data class CategoryWithMovies(

    @Embedded val categoryFavorite: CategoryFavorite,

    @Relation(
        parentColumn = "categoryId",
        entityColumn = "id",
        associateBy = Junction(CategoryMovieCrossRef::class)
    )
    val movieList: List<Movie>

)
