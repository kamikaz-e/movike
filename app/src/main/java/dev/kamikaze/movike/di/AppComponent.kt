@file:Suppress("unused")

package dev.kamikaze.movike.di

import android.app.Application
import dagger.BindsInstance
import dagger.Component
import dagger.android.AndroidInjectionModule
import dagger.android.AndroidInjector
import dagger.android.DaggerApplication
import dev.kamikaze.movike.di.modules.ActivityModule
import dev.kamikaze.movike.di.modules.AppModule
import dev.kamikaze.movike.di.annotations.qualifier.ApiQualifier
import javax.inject.Singleton

@Component(
    modules = [
        AndroidInjectionModule::class,
        AppModule::class,
        ActivityModule::class,
    ]
)
@Singleton
interface AppComponent : AndroidInjector<DaggerApplication> {

    @Component.Builder
    interface Builder {

        @BindsInstance
        fun application(application: Application): Builder

        @BindsInstance
        fun apiKey(@ApiQualifier apiKey: String): Builder

        fun build(): AppComponent
    }

}

