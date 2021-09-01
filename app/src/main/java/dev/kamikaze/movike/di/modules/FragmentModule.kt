package dev.kamikaze.movike.di.modules

import dev.kamikaze.movike.presentation.ui.fragments.FeedFragment
import dev.kamikaze.movike.presentation.ui.fragments.DetailsFragment
import dev.kamikaze.movike.presentation.ui.fragments.ProfileFragment
import dev.kamikaze.movike.presentation.ui.fragments.SearchFragment
import dagger.Module
import dagger.android.ContributesAndroidInjector

@Module
abstract class FragmentModule {

    @ContributesAndroidInjector
    abstract fun contributeFeedFragment(): FeedFragment

    @ContributesAndroidInjector
    abstract fun contributeMovieFragment(): DetailsFragment

    @ContributesAndroidInjector
    abstract fun contributeSearchFragment(): SearchFragment

    @ContributesAndroidInjector
    abstract fun contributeProfileFragment(): ProfileFragment

}