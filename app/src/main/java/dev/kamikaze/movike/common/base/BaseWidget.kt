package dev.kamikaze.movike.common.base

import android.content.Context
import android.util.AttributeSet
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.FrameLayout

abstract class BaseWidget<MODEL, CALLBACK>(context: Context, attrs: AttributeSet) : FrameLayout(context, attrs) {

    var model: MODEL? = null

    var callback: CALLBACK? = null

    var isVisible = true

    abstract fun onCreateView(inflater: LayoutInflater, container: ViewGroup): View

    abstract fun onBindView()

}