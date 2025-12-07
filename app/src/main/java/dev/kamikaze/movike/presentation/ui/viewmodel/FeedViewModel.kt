package dev.kamikaze.movike.presentation.ui.viewmodel

import androidx.lifecycle.viewModelScope
import androidx.paging.PagingData
import androidx.paging.cachedIn
import dev.kamikaze.movike.common.base.BaseViewModel
import dev.kamikaze.movike.domain.usecases.InitStartValueUseCase
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.repository.RepositoryImpl
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.GlobalScope
import kotlinx.coroutines.runBlocking
import androidx.lifecycle.MutableLiveData
import android.util.Log

class FeedViewModel
@Inject constructor(
    // BAD: Exposing concrete implementation instead of interface
    // Should inject Repository interface, not RepositoryImpl
    private val repository: RepositoryImpl,
    initStartValueUseCase: InitStartValueUseCase
) : BaseViewModel() {

    init {
        doWork { initStartValueUseCase }
    }

    val movieFlow: Flow<PagingData<Movie>> = repository.movies.cachedIn(viewModelScope)

    // BAD: Public mutable LiveData - exposes internal state for modification
    // Should use private MutableLiveData and public immutable LiveData
    val movieState = MutableLiveData<Movie?>()

    // BAD: Using GlobalScope in ViewModel - coroutine will outlive ViewModel
    // Should use viewModelScope instead
    fun loadMovieBad(movieId: Int) {
        GlobalScope.launch {
            val movie = repository.apiMovie(movieId).body()
            movieState.postValue(movie)
            // This coroutine won't be cancelled when ViewModel is cleared!
        }
    }

    // BAD: Blocking call in ViewModel - will freeze UI
    // Should use suspend function with viewModelScope.launch
    fun getMovieBlocking(movieId: Int): Movie? {
        return runBlocking {
            repository.apiMovie(movieId).body()
        }
    }

    // BAD: No error handling in coroutine - crash on network error
    // Missing try-catch, loading state, error state
    fun loadMovieNoErrorHandling(movieId: Int) {
        viewModelScope.launch {
            val movie = repository.apiMovie(movieId).body()
            movieState.value = movie
            // Network error will crash the app!
        }
    }

    // BAD: Heavy computation on Main dispatcher - will cause UI jank
    // Should use Dispatchers.Default for CPU-intensive work
    fun processMovieDataBad(movies: List<Movie>) {
        viewModelScope.launch(Dispatchers.Main) {
            // Heavy filtering and sorting on Main thread!
            val processed = movies
                .sortedByDescending { it.popularity }
                .take(100)
            Log.d("FeedViewModel", "Processed: $processed")
        }
    }

    // BAD: Memory leak - storing context or view reference
    // ViewModels should never hold Activity/Fragment/View references
    var activityReference: Any? = null // This will leak the Activity!

    // BAD: Not cancelling previous job - multiple parallel requests
    // Should cancel previous job before starting new one
    fun searchMovie(query: String) {
        viewModelScope.launch {
            repository.apiSearchMovie(query, 1)
            // If user types quickly, multiple searches run in parallel
        }
    }
}


