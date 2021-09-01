package dev.kamikaze.movike.presentation.customviews

import android.content.Context
import android.util.AttributeSet
import androidx.swiperefreshlayout.widget.SwipeRefreshLayout
import dev.kamikaze.movike.R

class CustomSwipeRefreshLayout(context: Context, attrs: AttributeSet) :
    SwipeRefreshLayout(context, attrs), SwipeRefreshLayout.OnRefreshListener {

    var callback: OnRefreshListener? = null

    init {
        setColorSchemeResources(R.color.orange, R.color.light_red, R.color.red)
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
