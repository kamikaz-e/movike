package dev.kamikaze.movike.di.modules

import dev.kamikaze.movike.presentation.ui.activity.SingleActivity
import dagger.Module
import dagger.android.ContributesAndroidInjector

@Module
abstract class ActivityModule {

    @ContributesAndroidInjector(modules = [FragmentModule::class])
    abstract fun contributeMainActivity(): SingleActivity

}