package dev.kamikaze.movike.presentation.ui.viewmodel

import dev.kamikaze.movike.common.base.BaseUiState
import dev.kamikaze.movike.common.base.BaseViewModel
import dev.kamikaze.movike.domain.usecases.CheckMovieAsWatchUseCase
import dev.kamikaze.movike.domain.usecases.SaveMovieAsWatchUseCase
import dev.kamikaze.movike.models.room.entity.Movie
import dev.kamikaze.movike.repository.RepositoryImpl
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.asStateFlow
import javax.inject.Inject

class DetailsMovieViewModel
@Inject constructor(
    private val repository: RepositoryImpl,
    private val saveMovieUseCase: SaveMovieAsWatchUseCase,
    private val checkMovieUseCase: CheckMovieAsWatchUseCase
) : BaseViewModel() {

    private var movie = Movie()

    private val _uiState = MutableStateFlow<BaseUiState>(BaseUiState.Success(movie))
    val uiState = _uiState.asStateFlow()

    private val _isWatchBtn = MutableStateFlow(false)
    val isWatchBtn = _isWatchBtn.asStateFlow()

    fun onLoadMovie(id: Int) {
        safeApiCall({ repository.apiMovie(id) },
            onSuccess = { onSuccessLoad(it) },
            onError = { onError(it) }
        )
    }

    fun onSeeClick() {
        doWork {
            _isWatchBtn.value = saveMovieUseCase(movie)
        }
    }

    private fun onSuccessLoad(receiveMovie: Movie) {
        movie = receiveMovie
        _uiState.value = BaseUiState.Success(receiveMovie)
        doWork {
            _isWatchBtn.value = checkMovieUseCase(movie)
        }
    }

    private fun onError(throwable: Throwable) {
        _uiState.value = BaseUiState.Error(throwable)
    }

}
