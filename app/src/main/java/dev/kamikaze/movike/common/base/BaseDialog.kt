package dev.kamikaze.movike.common.base

import androidx.fragment.app.DialogFragment
import dev.kamikaze.movike.presentation.ui.activity.SingleActivity

abstract class BaseDialog : DialogFragment(), BaseDialogView {

    val parent get() = parentFragment as BaseFragment<BaseNavigator>

    override fun getContext() = activity as SingleActivity

}
