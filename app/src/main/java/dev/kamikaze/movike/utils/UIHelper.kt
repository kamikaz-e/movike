package dev.kamikaze.movike.utils

import android.content.Context
import android.content.res.Configuration
import android.graphics.Typeface
import androidx.annotation.*
import androidx.core.content.ContextCompat
import androidx.core.content.res.ResourcesCompat
import dev.kamikaze.movike.R
import dev.kamikaze.movike.AppController

object UIHelper {

    fun getDimen(@DimenRes dimenRes: Int) =
        AppController.appContext.resources.getDimensionPixelSize(dimenRes)

    val defaultFont: Typeface?
        get() = ResourcesCompat.getFont(AppController.appContext, R.font.movike_regular)

    fun getDraw(@DrawableRes drawRes: Int) =
        ContextCompat.getDrawable(AppController.appContext, drawRes)

    fun getArray(@ArrayRes arrayRes: Int): Array<String> =
        AppController.appContext.resources.getStringArray(arrayRes)

    fun getStr(@StringRes stringRes: Int) = AppController.appContext.getString(stringRes)

    fun getStr(strId: Int, vararg param: String) = AppController.appContext.getString(strId, *param)

    fun getClr(@ColorRes colorRes: Int) = ContextCompat.getColor(AppController.appContext, colorRes)

    fun getScreenOrientation(context: Context): Int {
        return if (getScreenWidth(context) < getScreenHeight(context)) {
            Configuration.ORIENTATION_PORTRAIT
        } else {
            Configuration.ORIENTATION_LANDSCAPE
        }
    }

    fun getScreenWidth(context: Context?): Int {
        return if (context == null) 0 else getDisplayMetrics(context).widthPixels
    }

    fun getScreenHeight(context: Context?): Int {
        return if (context == null) 0 else getDisplayMetrics(context).heightPixels
    }

    fun getDisplayMetrics(context: Context) = context.resources.displayMetrics

}