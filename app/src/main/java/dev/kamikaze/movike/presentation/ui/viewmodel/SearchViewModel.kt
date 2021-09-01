package dev.kamikaze.movike.presentation.ui.viewmodel

import androidx.lifecycle.viewModelScope
import androidx.paging.PagingData
import androidx.paging.cachedIn
import dev.kamikaze.movike.common.base.BaseViewModel
import dev.kamikaze.movike.repository.RepositoryImpl
import dev.kamikaze.movike.models.room.entity.Movie
import kotlinx.coroutines.flow.Flow
import javax.inject.Inject

class SearchViewModel
@Inject constructor(
    private val repository: RepositoryImpl
) : BaseViewModel() {

    fun getMovieFlow(searchString: String): Flow<PagingData<Movie>> {
        return repository.getSearchMovieItems(searchString).cachedIn(viewModelScope)
    }

}