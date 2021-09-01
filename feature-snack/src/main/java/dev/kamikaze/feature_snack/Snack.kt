package dev.kamikaze.feature_snack

import android.view.View
import android.view.ViewGroup
import com.google.android.material.snackbar.BaseTransientBottomBar
import dev.kamikaze.feature_snack.base.BaseSnack
import dev.kamikaze.feature_snack.insets.navigationBarHeight

class Snack<S : BaseSnack>(
    parent: ViewGroup,
    private val content: S
) : BaseTransientBottomBar<Snack<S>>(parent, content as View, content) {

    init {
        view.setPadding(0, 0, 0, view.context.navigationBarHeight)
    }

    fun show(stringText: String?) {
        content.setTitle(stringText)
        show()
    }

    fun show(titleText: String?, btnText: String?, callback: View.OnClickListener) {
        content.apply {
            setTitle(titleText)
            setTextBtn(btnText)
            setCallback(callback)
        }
        show()
    }

}