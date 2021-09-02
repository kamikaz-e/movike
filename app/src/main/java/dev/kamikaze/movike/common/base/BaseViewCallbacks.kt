package dev.kamikaze.movike.common.base

import androidx.annotation.StringRes
import dev.kamikaze.movike.presentation.customviews.error.ErrorCallback

interface BaseViewCallbacks : ErrorCallback {

    fun showProgress()
    fun hideProgress()

    fun showError(throwable: Throwable)
    fun showError()
    fun hideError()

    fun setTitle(titleString: String?)
    fun setTitle(@StringRes titleRes: Int)
    
    fun showToolbar()
    fun hideToolbar()
    
    fun onLoading()
    fun onLoadFinish()

}