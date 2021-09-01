package dev.kamikaze.movike.presentation.navigation.navigators

import dev.kamikaze.movike.common.base.BaseNavigator

interface FeedNavigator : BaseNavigator {

    fun goToDetailsMovie(movieId: Int)

    fun goToSearchMovies()

}