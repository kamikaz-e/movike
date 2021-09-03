package dev.kamikaze.movike.presentation.ui.activity

import dev.kamikaze.movike.presentation.customviews.error.ErrorCallback
import dev.kamikaze.shared_error.ApiError

interface SingleActivityViewModelCallbacks {
    
    fun startGooglePlay()
    
    fun showProgress()
    
    fun hideProgress()
    
    fun setError(isShowError: Boolean, error: ApiError?)
    
    fun setOnErrorClick(callback: ErrorCallback?)
    
    fun hideToolbar()
    
    fun showToolbar()
    
}