package dev.kamikaze.movike.di.modules

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import dev.kamikaze.movike.di.annotations.scope.ViewModelKey
import dev.kamikaze.movike.presentation.ui.viewmodel.factory.ViewModelFactory
import dev.kamikaze.movike.presentation.ui.viewmodel.FeedViewModel
import dev.kamikaze.movike.presentation.ui.viewmodel.DetailsMovieViewModel
import dev.kamikaze.movike.presentation.ui.viewmodel.ProfileViewModel
import dev.kamikaze.movike.presentation.ui.viewmodel.SearchViewModel
import dagger.Binds
import dagger.Module
import dagger.multibindings.IntoMap

@Module
abstract class ViewModelModule {

    @Binds
    abstract fun bindViewModelFactory(factory: ViewModelFactory): ViewModelProvider.Factory

    @Binds
    @IntoMap
    @ViewModelKey(FeedViewModel::class)
    abstract fun bindFeedViewModel(feedViewModel: FeedViewModel): ViewModel

    @Binds
    @IntoMap
    @ViewModelKey(DetailsMovieViewModel::class)
    abstract fun bindMovieViewModel(movieViewModel: DetailsMovieViewModel): ViewModel

    @Binds
    @IntoMap
    @ViewModelKey(SearchViewModel::class)
    abstract fun bindSearchViewModel(searchViewModel: SearchViewModel): ViewModel

    @Binds
    @IntoMap
    @ViewModelKey(ProfileViewModel::class)
    abstract fun bindProfileViewModel(profileViewModel: ProfileViewModel): ViewModel

}
