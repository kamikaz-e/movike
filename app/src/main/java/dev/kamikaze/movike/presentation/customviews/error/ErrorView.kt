package dev.kamikaze.movike.presentation.customviews.error

import android.content.Context
import android.util.AttributeSet
import android.view.LayoutInflater
import android.view.View
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.core.view.isVisible
import dev.kamikaze.movike.databinding.CustomViewErrorBinding
import dev.kamikaze.shared_error.ApiError

class ErrorView(context: Context, attrs: AttributeSet) :
    ConstraintLayout(context, attrs), View.OnClickListener {

    private var _binding: CustomViewErrorBinding? = null
    private val binding by lazy { _binding!! }

    var errorCallback: ErrorCallback? = null

    init {
        _binding = CustomViewErrorBinding.inflate(LayoutInflater.from(context), this, true)
        binding.retryTV.setOnClickListener(this)
    }

    override fun onClick(view: View) {
        errorCallback?.onRetryLoad()
    }

    fun initParams(isShowError: Boolean, error: ApiError?) {
        isVisible = isShowError
        error?.apply {
            binding.apply {
                titleTV.text = titleText
                subtitleTV.text = subtitleText
            }
        }
    }

    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        _binding = null
    }

}