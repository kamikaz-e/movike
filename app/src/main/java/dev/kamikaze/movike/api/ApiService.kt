package dev.kamikaze.movike.api

import dev.kamikaze.movike.models.retrofit.response.MovieListResponse
import dev.kamikaze.movike.models.room.entity.Movie
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface ApiService {

    @GET("discover/movie")
    suspend fun apiMainMovie(
        @Query("page") page: Int
    ): MovieListResponse

    @GET("search/movie")
    suspend fun apiSearchMovie(
        @Query("query") query: String,
        @Query("page") page: Int
    ): MovieListResponse

    @GET("movie/{movie_id}")
    suspend fun apiMovie(
        @Path("movie_id") movieId: Int
    ): Response<Movie>
}