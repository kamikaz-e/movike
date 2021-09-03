package dev.kamikaze.movike.common.base

import dev.kamikaze.movike.presentation.customviews.error.ErrorCallback

interface BaseViewCallbacks : ErrorCallback {
    
    fun showProgress()
    fun hideProgress()
    
    fun showError(throwable: Throwable)
    fun showError()
    fun hideError()
    
    fun onLoading()
    fun onLoadFinish()
    
}