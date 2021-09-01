@file:Suppress("unused")

package dev.kamikaze.feature_snack

import android.app.Activity
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.annotation.StringRes
import androidx.fragment.app.Fragment
import dev.kamikaze.feature_snack.base.BaseSnack
import dev.kamikaze.feature_snack.view.SnackCallbackView
import dev.kamikaze.feature_snack.view.SnackView

fun <S : BaseSnack> instanceSnack(viewGroup: ViewGroup, snackView: S): Snack<S> {
    val customView = LayoutInflater.from(viewGroup.context).inflate(
        snackView.layoutId, viewGroup, false
    ) as S
    return Snack(viewGroup, customView)
}

fun Activity.showSnack(text: String?) {
    val rootView = window?.decorView as ViewGroup
    val snack = instanceSnack(rootView, SnackView(this))
    snack.show(text)
}

fun Activity.showSnack(@StringRes titleResId: Int) {
    showSnack(getString(titleResId))
}

fun Activity.showSnackCallback(
    titleText: String?,
    btnText: String?,
    callback: View.OnClickListener
) {
    val rootView = window?.decorView as ViewGroup
    val snack = instanceSnack(rootView, SnackCallbackView(this))
    snack.show(titleText, btnText, callback)
}

fun Activity.showSnackCallback(
    titleText: String?,
    @StringRes btnResId: Int,
    callback: View.OnClickListener
) {
    val rootView = window?.decorView as ViewGroup
    val snack = instanceSnack(rootView, SnackCallbackView(this))
    snack.show(titleText, getString(btnResId), callback)
}

fun Activity.showSnackCallback(
    @StringRes titleResId: Int,
    @StringRes btnResId: Int,
    callback: View.OnClickListener
) {
    showSnackCallback(getString(titleResId), btnResId, callback)
}

fun Fragment.showSnack(text: String) {
    activity?.showSnack(text)
}

fun Fragment.showSnack(@StringRes titleResId: Int) {
    showSnack(getString(titleResId))
}

fun Fragment.showSnackCallback(
    titleText: String?,
    btnText: String?,
    callback: View.OnClickListener
) {
    activity?.showSnackCallback(titleText, btnText, callback)
}

fun Fragment.showSnackCallback(
    titleText: String?,
    @StringRes btnResId: Int,
    callback: View.OnClickListener
) {
    activity?.showSnackCallback(titleText, btnResId, callback)
}

fun Fragment.showSnackCallback(
    @StringRes titleResId: Int,
    @StringRes btnResId: Int,
    callback: View.OnClickListener
) {
    activity?.showSnackCallback(titleResId, btnResId, callback)
}

