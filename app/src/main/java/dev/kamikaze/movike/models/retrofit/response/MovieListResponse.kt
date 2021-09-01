package dev.kamikaze.movike.models.retrofit.response

import dev.kamikaze.movike.models.room.entity.Movie
import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
class MovieListResponse(

    @SerialName("results")
    var itemList: List<Movie> = listOf(),
    var page: Int = 0,
    var total_results: Int = 0,
    var total_pages: Int = 0

)

