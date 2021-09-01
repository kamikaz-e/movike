@file:Suppress("unused")

package dev.kamikaze.shared_utils.extensions

import android.content.Context
import android.os.Build
import android.view.WindowInsets
import android.view.WindowManager

val Context.navigationBarHeight: Int
    get() {
        val windowManager = getSystemService(Context.WINDOW_SERVICE) as WindowManager
        return if (Build.VERSION.SDK_INT >= 30) {
            windowManager
                .currentWindowMetrics
                .windowInsets
                .getInsets(WindowInsets.Type.navigationBars())
                .bottom

        } else {
            return supportNavigationBarHeight
        }
    }

val Context.statusBarHeight: Int
    get() {
        val resourceId = resources.getIdentifier("status_bar_height", "dimen", "android")
        if (resourceId > 0) {
            return resources.getDimensionPixelSize(resourceId)
        }
        return 0
    }

private val Context.supportNavigationBarHeight: Int
    get() {
        val resourceId = resources.getIdentifier("navigation_bar_height", "dimen", "android")
        if (resourceId > 0) {
            return resources.getDimensionPixelSize(resourceId)
        }
        return 0
    }