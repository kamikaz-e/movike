package dev.kamikaze.movike.presentation.customviews

import android.content.Context
import android.util.AttributeSet
import android.view.LayoutInflater
import android.widget.FrameLayout
import android.widget.TextView
import dev.kamikaze.movike.R
import dev.kamikaze.movike.utils.UIHelper

class WatchMovieBtn(context: Context, attrs: AttributeSet) : FrameLayout(context, attrs) {

    var callback: WatchCallback? = null

    private val view by lazy {
        LayoutInflater.from(context).inflate(R.layout.view_watch_movie, this)
    }

    private val watchView by lazy { view.findViewById<TextView>(R.id.watchTV) }

    private val enableState = Triple(
        R.drawable.bgr_circle_orange_ripple_light_orange,
        R.color.black_dark,
        R.drawable.ic_favorite_black
    )

    private val disableState = Triple(
        R.drawable.bgr_circle_black_ripple_grey,
        R.color.white_light,
        R.drawable.ic_favorite_white
    )

    init {
        watchView.setOnClickListener { callback?.onWatchClicked() }
    }

    fun renderSaveBtn(isActiveBtn: Boolean) {
        val btnViewRes = if (isActiveBtn) enableState else disableState
        watchView.apply {
            setBackgroundResource(btnViewRes.first)
            setTextColor(UIHelper.getClr(btnViewRes.second))
            setCompoundDrawablesWithIntrinsicBounds(btnViewRes.third, 0, 0, 0)
        }
    }

    interface WatchCallback {
        fun onWatchClicked()
    }

}