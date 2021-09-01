package dev.kamikaze.movike.di.modules

import android.app.Application
import android.content.Context
import android.content.SharedPreferences
import dagger.Module
import dagger.Provides
import javax.inject.Singleton

@Module
class PreferencesModule {

    @Singleton
    @Provides
    fun providePref(app: Application): SharedPreferences {
        return app.getSharedPreferences("SharedPreferences", Context.MODE_PRIVATE)
    }

}