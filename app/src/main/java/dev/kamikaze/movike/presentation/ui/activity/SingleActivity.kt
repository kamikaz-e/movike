package dev.kamikaze.movike.presentation.ui.activity

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.appcompat.widget.Toolbar
import androidx.core.view.isVisible
import dagger.android.support.DaggerAppCompatActivity
import dev.kamikaze.movike.BuildConfig
import dev.kamikaze.movike.common.base.NavigatorProvider
import dev.kamikaze.movike.databinding.ActivityMainBinding
import dev.kamikaze.movike.presentation.customviews.error.ErrorCallback
import dev.kamikaze.movike.presentation.navigation.Navigator
import dev.kamikaze.shared_error.ApiError

class SingleActivity : DaggerAppCompatActivity(), SingleActivityViewModelCallbacks, NavigatorProvider {
    
    private val binding: ActivityMainBinding by lazy { ActivityMainBinding.inflate(layoutInflater) }
    
    private val toolbar: Toolbar by lazy { binding.toolbar }
    
    override val navigator: Navigator by lazy { Navigator(this, toolbar) }
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(binding.root)
    }
    
    override fun onSupportNavigateUp(): Boolean {
        return navigator.supportNavigateToolbar() || super.onSupportNavigateUp()
    }
    
    override fun startGooglePlay() {
        startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(BuildConfig.APP_LINK)))
    }
    
    override fun showProgress() {
        binding.progressBar.show()
    }
    
    override fun hideProgress() {
        binding.progressBar.hide()
    }
    
    override fun setError(isShowError: Boolean, error: ApiError?) {
        binding.apply {
            progressBar.isVisible = !isShowError
            navHostFragment.isVisible = !isShowError
            errorView.initParams(isShowError, error)
        }
    }
    
    override fun setOnErrorClick(callback: ErrorCallback?) {
        binding.errorView.errorCallback = callback
    }
    
    override fun setTitle(titleString: String?) {
        toolbar.title = title
    }
    
    override fun hideToolbar() {
        toolbar.isVisible = false
    }
    
    override fun showToolbar() {
        toolbar.isVisible = true
    }
    
}
