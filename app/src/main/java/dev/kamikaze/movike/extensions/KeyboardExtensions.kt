@file:Suppress("unused")

package dev.kamikaze.movike.extensions

import android.app.Activity
import android.app.Dialog
import android.content.Context
import android.view.View
import androidx.fragment.app.Fragment
import dev.kamikaze.movike.common.base.BaseFragment
import dev.kamikaze.movike.common.base.BaseNavigator
import dev.kamikaze.movike.utils.KeyboardUtil

fun Context.showAppKeyboard(view: View) {
    KeyboardUtil.showKeyboard(view, this)
}

fun Activity.showAppKeyboard(view: View) {
    KeyboardUtil.showKeyboard(view, this)
}

fun Fragment.showAppKeyboard(view: View) {
    requireContext().showAppKeyboard(view)
}

fun View.showAppKeyboard(view: View) {
    context.showAppKeyboard(view)
}

fun Dialog.showAppKeyboard() {
    KeyboardUtil.showKeyboardFromDialog(this)
}

fun Activity.hideAppKeyboard() {
    KeyboardUtil.hideKeyboard(this)
}

fun BaseFragment<BaseNavigator>.hideAppKeyboard() {
    requireActivity().hideAppKeyboard()
}

fun View.hideAppKeyboard() {
    KeyboardUtil.hideKeyboard(this)
}

fun Dialog.hideAppKeyboard() {
    KeyboardUtil.hideKeyboardFromDialog(this)
}

fun Context.hideKeyBoardClickOutSide(view: View) {
    KeyboardUtil.hideKeyBoardClickOutSide(view, this)
}

fun Activity.hideKeyBoardClickOutSide(view: View) {
    KeyboardUtil.hideKeyBoardClickOutSide(view, this)
}

fun Fragment.hideKeyBoardClickOutSide(view: View) {
    requireContext().hideKeyBoardClickOutSide(view)
}

fun View.hideKeyBoardClickOutSide(view: View) {
    context.hideKeyBoardClickOutSide(view)
}
