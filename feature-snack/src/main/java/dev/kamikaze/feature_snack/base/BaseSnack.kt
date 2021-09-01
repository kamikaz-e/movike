package dev.kamikaze.feature_snack.base

import android.view.View
import com.google.android.material.snackbar.ContentViewCallback

interface BaseSnack : ContentViewCallback {

    val view: View

    val layoutId: Int

    fun setTitle(titleText: String?)

    fun setTextBtn(btnText: String?)

    fun setCallback(callback: View.OnClickListener)

}