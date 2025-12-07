package dev.kamikaze.movike.di.modules

import androidx.lifecycle.ViewModel
import dagger.Binds
import dagger.Module
import dagger.multibindings.IntoMap
import dev.kamikaze.movike.di.annotations.scope.ViewModelKey
import dev.kamikaze.movike.presentation.ui.compose.assistant.AssistantChatViewModel

@Module
abstract class AssistantModule {

    @Binds
    @IntoMap
    @ViewModelKey(AssistantChatViewModel::class)
    abstract fun bindAssistantChatViewModel(viewModel: AssistantChatViewModel): ViewModel

}
