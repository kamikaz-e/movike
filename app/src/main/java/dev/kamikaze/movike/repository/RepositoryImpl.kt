package dev.kamikaze.movike.repository

import androidx.paging.Pager
import androidx.paging.PagingData
import dev.kamikaze.movike.api.ApiService
import dev.kamikaze.movike.utils.PagingConfigs
import dev.kamikaze.movike.data.database.DatabaseInterface
import dev.kamikaze.movike.data.datasource.FeedPagingDataSource
import dev.kamikaze.movike.data.datasource.SearchPagingDataSource
import dev.kamikaze.movike.models.retrofit.response.MovieListResponse
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.models.room.relate.CategoryWithMovies
import dev.kamikaze.movike.models.room.relate.MovieWithCategories
import kotlinx.coroutines.flow.Flow
import retrofit2.Response
import javax.inject.Inject

class RepositoryImpl
@Inject constructor(
    private val apiService: ApiService,
    private val database: DatabaseInterface
) : Repository {

    override val movies: Flow<PagingData<Movie>>
        get() = Pager(
            PagingConfigs.defaultPagingConfig,
            pagingSourceFactory = { FeedPagingDataSource(apiService) }
        ).flow

    override fun getSearchMovieItems(searchString: String): Flow<PagingData<Movie>> = Pager(
        PagingConfigs.defaultPagingConfig,
        pagingSourceFactory = { SearchPagingDataSource(apiService, searchString) }
    ).flow

    /* override var apiKey: String
         get() = appPreferences.apiKey
         set(value) {
             appPreferences.apiKey = value
         }
 */
    override val moviesWithCategory: List<MovieWithCategories>
        get() = database.moviesWithCategory

    override val categoriesFavorite: List<CategoryWithMovies>
        get() = database.categoriesFavorite

    override fun initStartValue() {
        return database.initStartValue()
    }

    override suspend fun apiMainMovie(page: Int): MovieListResponse {
        return apiService.apiMainMovie(page)
    }

    override suspend fun apiSearchMovie(query: String, page: Int): MovieListResponse {
        return apiService.apiSearchMovie(query, page)
    }

    override suspend fun apiMovie(movieId: Int): Response<Movie> {
        return apiService.apiMovie(movieId)
    }

    override fun saveMovieAsWatch(movie: Movie): Boolean {
        return database.saveMovieAsWatch(movie)
    }

    override fun isWatchMovieCheck(movie: Movie): Boolean {
        return database.isWatchMovieCheck(movie)
    }

}
