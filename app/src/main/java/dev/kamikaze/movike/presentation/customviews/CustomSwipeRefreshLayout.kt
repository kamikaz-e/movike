package dev.kamikaze.movike.presentation.customviews

import android.content.Context
import android.util.AttributeSet
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import dev.kamikaze.movike.R
import dev.kamikaze.shared_extensions.R as SharedR

class CustomSwipeRefreshLayout(context: Context, attrs: AttributeSet) :
    SwipeRefreshLayout(context, attrs), SwipeRefreshLayout.OnRefreshListener {

    var callback: OnRefreshListener? = null

    init {
        setColorSchemeResources(SharedR.color.orange, SharedR.color.light_red, SharedR.color.red)
        setOnRefreshListener(this)
    }

    override fun onRefresh() {
        callback?.onRefresh()
    }

    fun showProgress() {
        isRefreshing = true
    }

    fun hideProgress() {
        isRefreshing = false
    }

}
