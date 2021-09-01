package dev.kamikaze.movike.common.base

import android.content.Context
import android.os.Bundle
import android.view.View
import androidx.annotation.StringRes
import dagger.android.support.DaggerFragment
import dev.kamikaze.feature_snack.showSnackCallback
import dev.kamikaze.movike.presentation.ui.activity.SingleActivityViewModelCallbacks
import dev.kamikaze.movike.utils.KeyboardUtil.hideKeyboard
import dev.kamikaze.shared_error.ApiError
import dev.kamikaze.shared_error.ApiErrorFactory
import kotlinx.serialization.ExperimentalSerializationApi

abstract class BaseFragment<N : BaseNavigator> : DaggerFragment(), BaseViewCallbacks {

    protected var callbacks: SingleActivityViewModelCallbacks? = null

    private var navigatorInstance: N? = null
    protected val navigator: N by lazy { navigatorInstance!! }

    abstract fun initView()

    override fun onAttach(context: Context) {
        super.onAttach(context)
        if (context is SingleActivityViewModelCallbacks) {
            callbacks = context
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setHasOptionsMenu(false)
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        hideError()
        initView()
    }

    override fun onStart() {
        super.onStart()
        navigatorInstance = (requireActivity() as NavigatorProvider).provideNavigator() as N
    }

    override fun onResume() {
        super.onResume()
        callbacks?.setOnErrorClick(this)
    }

    override fun onPause() {
        super.onPause()
        hideKeyboard(requireActivity())
        callbacks?.setOnErrorClick(null)
    }

    override fun onStop() {
        super.onStop()
        navigatorInstance = null
    }

    override fun onDetach() {
        super.onDetach()
        callbacks = null
    }

    override fun showProgress() {
        callbacks?.showProgress()
    }

    override fun hideProgress() {
        callbacks?.hideProgress()
    }

    @ExperimentalSerializationApi
    override fun showError() {
        showError(Throwable())
    }

    @ExperimentalSerializationApi
    override fun showError(throwable: Throwable) {
        hideProgress()
        handleError(throwable)
    }

    override fun hideError() {
        callbacks?.setError(false, null)
    }

    override fun onLoading() {
        hideError()
        showProgress()
    }

    override fun onLoadFinish() {
        hideError()
        hideProgress()
    }

    override fun setTitle(titleString: String?) {
        callbacks?.setTitle(titleString)
    }

    override fun setTitle(@StringRes titleRes: Int) {
        setTitle(getString(titleRes))
    }

    private fun showError(error: ApiError) {
        callbacks?.setError(true, error)
    }

    @ExperimentalSerializationApi
    private fun handleError(throwable: Throwable) {
        val apiError = ApiErrorFactory(requireActivity()).handleError(throwable)
        showError(apiError)
    }

    private fun onUpgradeCodeReceived(apiError: ApiError) {
        showSnackCallback(apiError.titleText, apiError.btnName) { callbacks?.startGooglePlay() }
    }

}
