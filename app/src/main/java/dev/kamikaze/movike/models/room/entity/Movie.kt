package dev.kamikaze.movike.models.room.entity

import androidx.room.Entity
import androidx.room.PrimaryKey
import dev.kamikaze.movike.api.paths.ApiPaths
import dev.kamikaze.movike.utils.DateUtil
import dev.kamikaze.movike.utils.StringUtil
import kotlinx.serialization.Serializable

@Entity(tableName = "movie")
@Serializable
data class Movie(

    @PrimaryKey(autoGenerate = true)
    var id: Int = 0,
    var title: String = "",
    var vote_count: Int = 0,
    var vote_average: Float = 0F,
    var poster_path: String? = "",
    var release_date: String? = "",
    var backdrop_path: String? = "",
    var original_title: String? = null,
    var original_language: String? = null,
    var adult: Boolean = false,
    var video: Boolean = false,
    var popularity: Float = 0F,
    var overview: String? = ""

) {

    val ratingValue: String?
        get() = StringUtil.getStringRoundingNumber(vote_average, 1)

    val yearValue: String
        get() = DateUtil.getStringYear(release_date)

    val originalPosterPath: String
        get() = ApiPaths.getOriginalPosterPath(poster_path)

    val posterPath: String
        get() = ApiPaths.getPosterPath(poster_path)

    val backdropPath: String
        get() = ApiPaths.getBackdropPath(backdrop_path)

}

