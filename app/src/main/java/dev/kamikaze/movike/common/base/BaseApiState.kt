package dev.kamikaze.movike.common.base

import androidx.paging.PagingData
import dev.kamikaze.movike.models.room.entity.Movie

sealed class BaseApiState {

    object Loading : BaseApiState()

    object Empty : BaseApiState()

    class Success(val data: PagingData<Movie>) : BaseApiState()

    class Failure(val throwable: Throwable) : BaseApiState()

}