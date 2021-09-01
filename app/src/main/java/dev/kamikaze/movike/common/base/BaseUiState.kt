package dev.kamikaze.movike.common.base

sealed class BaseUiState {
    data class Success<M>(val value: M) : BaseUiState()
    data class Error(val throwable: Throwable) : BaseUiState()
}