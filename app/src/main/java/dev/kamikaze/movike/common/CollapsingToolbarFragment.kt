package dev.kamikaze.movike.common

import androidx.annotation.LayoutRes
import dev.kamikaze.movike.R
import dev.kamikaze.movike.common.base.BaseFragment
import dev.kamikaze.movike.common.base.BaseNavigator

abstract class CollapsingToolbarFragment<N : BaseNavigator>(
    @LayoutRes
    private val collapsingViewRes: Int? = R.layout.layout_default_collapsing_view
) : BaseFragment<N>() {

    override fun onStart() {
        super.onStart()
        callbacks?.supportCollapsingView(collapsingViewRes)
    }

    override fun onDestroyView() {
        super.onDestroyView()
        callbacks?.clearCollapsingView()
    }

}
