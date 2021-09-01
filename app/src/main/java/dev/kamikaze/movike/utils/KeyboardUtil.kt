package dev.kamikaze.movike.utils

import android.app.Activity
import android.app.Dialog
import android.content.Context
import android.view.View
import android.view.ViewGroup
import android.view.WindowManager
import android.view.inputmethod.InputMethodManager
import android.widget.Button
import android.widget.EditText
import android.widget.TextView

object KeyboardUtil {

    @Suppress("unused")
    fun showKeyboard(view: View, context: Context?) {
        if (view.requestFocus()) {
            val imm = context?.getSystemService(Activity.INPUT_METHOD_SERVICE) as InputMethodManager
            imm.showSoftInput(view, InputMethodManager.SHOW_FORCED)
        }
    }

    @Suppress("unused")
    fun hideKeyboard(view: View, context: Context?) {
        if (view.requestFocus()) {
            val imm = context?.getSystemService(Activity.INPUT_METHOD_SERVICE) as InputMethodManager
            imm.hideSoftInputFromWindow(view.windowToken, 0)

        }
    }

    @Suppress("unused")
    fun hideKeyboard(activity: Activity) {
        if (activity.currentFocus != null) {
            val imm = activity.getSystemService(Activity.INPUT_METHOD_SERVICE) as InputMethodManager
            imm.hideSoftInputFromWindow(activity.currentFocus?.windowToken, 0)
        }
    }

    @Suppress("unused")
    fun hideKeyboard(view: View) {
        if (!view.isFocusable) {
            val imm =
                view.context.getSystemService(Activity.INPUT_METHOD_SERVICE) as InputMethodManager
            imm.hideSoftInputFromWindow(view.windowToken, 0)
        }
    }

    @Suppress("unused")
    fun showKeyboardFromDialog(dialog: Dialog?) {
        dialog?.window?.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_VISIBLE)
    }

    @Suppress("unused")
    fun hideKeyboardFromDialog(dialog: Dialog?) {
        dialog?.window?.setSoftInputMode(WindowManager.LayoutParams.SOFT_INPUT_STATE_ALWAYS_HIDDEN)
    }

    @Suppress("unused")
    fun hideKeyBoardClickOutSide(view: View?, context: Context?) {
        view?.let {
            if (view !is TextView && view !is Button && view !is EditText) {
                view.setOnTouchListener { _, _ ->
                    view.performClick()
                    hideKeyboard(view)
                    false
                }
            }
            if (view is ViewGroup) {
                for (i in 0 until view.childCount) {
                    val innerView = view.getChildAt(i)
                    hideKeyBoardClickOutSide(innerView, context)
                }
            }
        }
    }

}
