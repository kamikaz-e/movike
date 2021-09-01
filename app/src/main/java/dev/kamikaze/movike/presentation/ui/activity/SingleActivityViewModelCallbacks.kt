package dev.kamikaze.movike.presentation.ui.activity

import androidx.annotation.LayoutRes
import dev.kamikaze.movike.presentation.customviews.error.ErrorCallback
import dev.kamikaze.shared_error.ApiError

interface SingleActivityViewModelCallbacks {

    fun startGooglePlay()

    fun showProgress()

    fun hideProgress()

    fun setError(isShowError: Boolean, error: ApiError?)

    fun setOnErrorClick(callback: ErrorCallback?)

    fun setTitle(titleString: String?)

    fun supportCollapsingView(@LayoutRes collapsingViewRes: Int?)

    fun clearCollapsingView()
}