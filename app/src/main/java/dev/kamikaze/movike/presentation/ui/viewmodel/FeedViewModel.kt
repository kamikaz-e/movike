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

class FeedViewModel
@Inject constructor(
    repository: RepositoryImpl,
    initStartValueUseCase: InitStartValueUseCase
) : BaseViewModel() {

    init {
        doWork { initStartValueUseCase }
    }

    val movieFlow: Flow<PagingData<Movie>> = repository.movies.cachedIn(viewModelScope)

}


