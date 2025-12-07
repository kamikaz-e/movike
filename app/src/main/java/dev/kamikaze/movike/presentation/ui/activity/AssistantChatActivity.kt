package dev.kamikaze.movike.presentation.ui.activity

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.lifecycle.ViewModelProvider
import dagger.android.AndroidInjection
import dev.kamikaze.movike.presentation.ui.compose.assistant.AssistantChatScreen
import dev.kamikaze.movike.presentation.ui.compose.assistant.AssistantChatViewModel
import dev.kamikaze.movike.presentation.ui.compose.theme.MovikeTheme
import javax.inject.Inject

/**
 * Activity for the Assistant Chat feature
 * Hosts the Jetpack Compose UI
 */
class AssistantChatActivity : ComponentActivity() {

    @Inject
    lateinit var viewModelFactory: ViewModelProvider.Factory

    private val viewModel: AssistantChatViewModel by lazy {
        ViewModelProvider(this, viewModelFactory)[AssistantChatViewModel::class.java]
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        AndroidInjection.inject(this)
        super.onCreate(savedInstanceState)

        setContent {
            MovikeTheme {
                Surface(color = MaterialTheme.colorScheme.background) {
                    AssistantChatScreen(
                        viewModel = viewModel,
                        onNavigateBack = { finish() }
                    )
                }
            }
        }
    }
}
