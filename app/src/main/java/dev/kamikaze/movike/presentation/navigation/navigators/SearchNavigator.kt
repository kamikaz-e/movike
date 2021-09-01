package dev.kamikaze.movike.presentation.navigation.navigators

import dev.kamikaze.movike.common.base.BaseNavigator

interface SearchNavigator : BaseNavigator {
    fun goToDetailsMovie(movieId: Int)
}