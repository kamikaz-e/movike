package dev.kamikaze.movike

import android.content.Context
import dagger.android.AndroidInjector
import dagger.android.DaggerApplication
import dev.kamikaze.movike.di.DaggerAppComponent

class AppController : DaggerApplication() {

    companion object {
        @Volatile
        lateinit var appContext: Context
            private set
    }

    private val appInjector = DaggerAppComponent.builder()
        .application(this)
        .apiKey(BuildConfig.API_KEY)
        .build()

    override fun applicationInjector(): AndroidInjector<out DaggerApplication> = appInjector

    override fun onCreate() {
        super.onCreate()
        appContext = applicationContext
    }

}