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

fun Context.showKeyboard(view: View) {
    KeyboardUtil.showKeyboard(view, this)
}

fun Activity.showKeyboard(view: View) {
    KeyboardUtil.showKeyboard(view, this)
}

fun Fragment.showKeyboard(view: View) {
    context?.showKeyboard(view)
}

fun View.showKeyboard(view: View) {
    context.showKeyboard(view)
}

fun Dialog.showKeyboard() {
    KeyboardUtil.showKeyboardFromDialog(this)
}

fun Activity.hideKeyboard() {
    KeyboardUtil.hideKeyboard(this)
}

fun BaseFragment<BaseNavigator>.hideKeyboard() {
    activity?.hideKeyboard()
}

fun View.hideKeyboard() {
    KeyboardUtil.hideKeyboard(this)
}

fun Dialog.hideKeyboard() {
    KeyboardUtil.hideKeyboardFromDialog(this)
}

fun Context.hideKeyBoardClickOutSide(view: View) {
    KeyboardUtil.hideKeyBoardClickOutSide(view, this)
}

fun Activity.hideKeyBoardClickOutSide(view: View) {
    KeyboardUtil.hideKeyBoardClickOutSide(view, this)
}

fun Fragment.hideKeyBoardClickOutSide(view: View) {
    context?.hideKeyBoardClickOutSide(view)
}

fun View.hideKeyBoardClickOutSide(view: View) {
    context.hideKeyBoardClickOutSide(view)
}
