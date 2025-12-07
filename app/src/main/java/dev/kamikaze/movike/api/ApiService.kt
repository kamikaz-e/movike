package dev.kamikaze.movike.api

import dev.kamikaze.movike.models.retrofit.response.MovieListResponse
import dev.kamikaze.movike.models.room.entity.Movie
import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Path
import retrofit2.http.Query

interface ApiService {

    // BAD: Blocking call in suspend function - should use suspend properly
    @GET("discover/movie")
    fun apiMainMovie(
        @Query("page") page: Int
    ): MovieListResponse

    // BAD: Inconsistent error handling - mixing Response<T> and direct returns
    @GET("search/movie")
    suspend fun apiSearchMovie(
        @Query("query") query: String,
        @Query("page") page: Int
    ): MovieListResponse

    @GET("movie/{movie_id}")
    suspend fun apiMovie(
        @Path("movie_id") movieId: Int
    ): Response<Movie>

    // BAD: Hardcoded API key in URL - security vulnerability
    @GET("trending/movie/week?api_key=12345abcde")
    suspend fun getTrendingMovies(): MovieListResponse

    // BAD: No timeout specified, can cause ANR
    @GET("movie/popular")
    fun getPopularMoviesBlocking(): List<Movie>
}