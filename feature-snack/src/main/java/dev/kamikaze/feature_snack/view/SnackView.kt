package dev.kamikaze.feature_snack.view

import android.content.Context
import android.util.AttributeSet
import android.view.LayoutInflater
import android.view.View
import android.widget.TextView
import androidx.constraintlayout.widget.ConstraintLayout
import dev.kamikaze.feature_snack.R
import dev.kamikaze.feature_snack.base.BaseSnack

class SnackView(
    context: Context, attributeSet: AttributeSet? = null
) : ConstraintLayout(context, attributeSet), BaseSnack {

    override val view: View by lazy {
        LayoutInflater.from(context).inflate(R.layout.view_snack, this)
    }
    override val layoutId = R.layout.layout_snack_view

    private val messageTV by lazy { view.findViewById<TextView>(R.id.messageTV) }

    override fun animateContentIn(delay: Int, duration: Int) {
        //animation
    }

    override fun animateContentOut(delay: Int, duration: Int) {
        //animation
    }

    override fun setTitle(titleText: String?) {
        messageTV.text = titleText
    }

    override fun setTextBtn(btnText: String?) {}

    override fun setCallback(callback: OnClickListener) {}

}