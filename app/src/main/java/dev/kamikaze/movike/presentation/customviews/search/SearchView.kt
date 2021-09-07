package dev.kamikaze.movike.presentation.customviews.search

import android.content.Context
import android.os.Bundle
import android.os.Parcelable
import android.text.Editable
import android.text.TextWatcher
import android.util.AttributeSet
import android.view.LayoutInflater
import android.view.ViewAnimationUtils
import android.view.animation.AccelerateInterpolator
import androidx.constraintlayout.widget.ConstraintLayout
import androidx.core.view.isVisible
import androidx.core.widget.doAfterTextChanged
import dev.kamikaze.movike.databinding.ViewSearchBinding
import dev.kamikaze.movike.extensions.showAppKeyboard
import dev.kamikaze.movike.utils.AppConstants

class SearchView(context: Context, attrs: AttributeSet) : ConstraintLayout(context, attrs) {
    
    private var _binding: ViewSearchBinding? = null
    private val binding by lazy { _binding!! }
    
    internal var callback: SearchCallback? = null
    
    private var isOpen = false
    private var searchObserver: TextWatcher? = null
    
    init {
        _binding = ViewSearchBinding.inflate(LayoutInflater.from(context), this, true)
        binding.apply {
            searchObserver = searchEditText.doAfterTextChanged { observeSearch(it) }
            clearBtn.setOnClickListener { onClearSearch() }
        }
        openSearch()
    }
    
    override fun onDetachedFromWindow() {
        super.onDetachedFromWindow()
        binding.apply { searchEditText.removeTextChangedListener(searchObserver) }
    }
    
    override fun onSaveInstanceState(): Parcelable {
        val bundle = Bundle()
        bundle.putParcelable(AppConstants.STATE, super.onSaveInstanceState())
        bundle.putBoolean(AppConstants.IS_OPEN, isOpen)
        return bundle
    }
    
    override fun onRestoreInstanceState(state: Parcelable?) {
        if (state is Bundle) {
            isOpen = state.getBoolean(AppConstants.IS_OPEN)
            super.onRestoreInstanceState(state.getParcelable(AppConstants.STATE))
        }
    }
    
    private fun observeSearch(searchValue: Editable?) {
        searchValue.toString().run {
            binding.clearBtn.isVisible = isNotEmpty()
            callback?.onSearch(this)
        }
    }
    
    private fun openSearch() {
        binding.apply {
            searchContainer.post {
                runAnimation()
                showAppKeyboard(searchEditText)
                searchContainer.isVisible = true
            }
        }
    }
    
    private fun onClearSearch() {
        binding.searchEditText.setText("")
    }
    
    private fun runAnimation() {
        val animTime = 243L
        if (!isOpen) {
            val startWidth = 0f
            val cX = width
            val cY = 0
            ViewAnimationUtils.createCircularReveal(
                    this, cX, cY, startWidth, width.toFloat()
            ).apply {
                interpolator = AccelerateInterpolator()
                duration = animTime
                start()
                isOpen = true
            }
        }
    }
    
}