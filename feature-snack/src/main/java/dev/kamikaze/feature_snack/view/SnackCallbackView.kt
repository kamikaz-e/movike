package dev.kamikaze.feature_snack.view

import android.content.Context
import android.util.AttributeSet
import android.view.View
import android.widget.TextView
import androidx.constraintlayout.widget.ConstraintLayout
import dev.kamikaze.feature_snack.R
import dev.kamikaze.feature_snack.base.BaseSnack

class SnackCallbackView(
    context: Context, attributeSet: AttributeSet? = null
) : ConstraintLayout(context, attributeSet), BaseSnack {

    override val view: View by lazy { View.inflate(context, R.layout.view_snack_callback, this) }
    override val layoutId = R.layout.layout_snack_callback_view

    private val messageTV by lazy { view.findViewById<TextView>(R.id.messageTV) }
    private val actionTV by lazy { view.findViewById<TextView>(R.id.actionTV) }

    override fun animateContentIn(delay: Int, duration: Int) {
        //animation
    }

    override fun animateContentOut(delay: Int, duration: Int) {
        //animation
    }

    override fun setTitle(titleText: String?) {
        messageTV.text = titleText
    }

    override fun setTextBtn(btnText: String?) {
        actionTV.text = btnText
    }

    override fun setCallback(callback: OnClickListener) {
        actionTV.setOnClickListener(callback)
    }

}