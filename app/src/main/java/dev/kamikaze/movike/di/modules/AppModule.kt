package dev.kamikaze.movike.di.modules

import android.content.Context
import dagger.Module
import dagger.Provides
import dev.kamikaze.movike.AppController
import dev.kamikaze.movike.api.ApiModule
import javax.inject.Singleton

@Module(
    includes = [
        ApiModule::class,
        DBModule::class,
        ViewModelModule::class,
        PreferencesModule::class,
        DataModule::class
    ]
)
class AppModule {

    @Provides
    @Singleton
    fun provideContext(appContext: AppController): Context = appContext

}