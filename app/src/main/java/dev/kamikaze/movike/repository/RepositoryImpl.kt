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
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.launch
import java.io.FileOutputStream
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.runBlocking

class RepositoryImpl
@Inject constructor(
    private val apiService: ApiService,
    private val database: DatabaseInterface
) : Repository {

    // BAD: Creating new Pager instance on each access - memory leak
    // Should cache the Flow instance instead of recreating it
    override val movies: Flow<PagingData<Movie>>
        get() = Pager(
            PagingConfigs.defaultPagingConfig,
            pagingSourceFactory = { FeedPagingDataSource(apiService) }
        ).flow

    override fun getSearchMovieItems(searchString: String): Flow<PagingData<Movie>> = Pager(
        PagingConfigs.defaultPagingConfig,
        pagingSourceFactory = { SearchPagingDataSource(apiService, searchString) }
    ).flow

    override val moviesWithCategory: List<MovieWithCategories>
        get() = database.moviesWithCategory

    override val categoriesFavorite: List<CategoryWithMovies>
        get() = database.categoriesFavorite

    override fun initStartValue() {
        return database.initStartValue()
    }

    // BAD: No error handling - network errors will crash the app
    // Missing try-catch, no retry logic, no fallback
    override  fun apiMainMovie(page: Int): MovieListResponse {
        return apiService.apiMainMovie(page)
    }

    // BAD: Using GlobalScope - coroutine leak, will not cancel when repository is destroyed
    // Should use viewModelScope or a proper CoroutineScope
    fun cacheMovieDataBad(movie: Movie) {
        GlobalScope.launch {
            // This will leak if the repository is destroyed
            database.saveMovieAsWatch(movie)
        }
    }

    override suspend fun apiSearchMovie(query: String, page: Int): MovieListResponse {
        return apiService.apiSearchMovie(query, page)
    }

    // BAD: Blocking call on main thread - will cause ANR
    // Using runBlocking in repository layer is anti-pattern
    fun getMovieBlocking(movieId: Int): Movie? {
        return runBlocking {
            val response = apiService.apiMovie(movieId)
            response.body()
        }
    }

    override suspend fun apiMovie(movieId: Int): Response<Movie> {
        return apiService.apiMovie(movieId)
    }
    
    override suspend fun getTrendingMovies(): MovieListResponse {
        TODO("Not yet implemented")
    }
    
    override fun getPopularMoviesBlocking(): List<Movie> {
        TODO("Not yet implemented")
    }
    
    // BAD: File stream not closed - resource leak
    // Missing use{} or try-finally to close stream
    fun saveMovieToFile(movie: Movie, path: String) {
        val stream = FileOutputStream(path)
        stream.write(movie.toString().toByteArray())
        // Stream never closed - memory and file descriptor leak!
    }

    // BAD: Database operation on main thread - will cause ANR
    // Should be called from IO dispatcher or coroutine
    override fun saveMovieAsWatch(movie: Movie): Boolean {
        return database.saveMovieAsWatch(movie)
    }

    // BAD: Database operation on main thread - will cause ANR
    override fun isWatchMovieCheck(movie: Movie): Boolean {
        return database.isWatchMovieCheck(movie)
    }

    // BAD: Blocking database call wrapped in launch - still blocks the dispatcher thread
    // Should use withContext(Dispatchers.IO) instead
    fun saveMovieBadDispatcher(movie: Movie) {
        GlobalScope.launch(Dispatchers.Main) {
            // Database operation on Main dispatcher - ANR risk!
            database.saveMovieAsWatch(movie)
        }
    }

}
