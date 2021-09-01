package dev.kamikaze.shared_error.util

import android.content.Context
import android.net.ConnectivityManager
import android.net.NetworkCapabilities
import android.os.Build

class ConnectNetworkUtil(
    private val context: Context
) {

    val isConnected: Boolean
        get() {
            var result = -1
            val cm = context.getSystemService(Context.CONNECTIVITY_SERVICE) as ConnectivityManager
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                cm.getNetworkCapabilities(cm.activeNetwork)?.run {
                    result = when {
                        hasTransport(NetworkCapabilities.TRANSPORT_VPN) -> NetworkCapabilities.TRANSPORT_VPN
                        hasTransport(NetworkCapabilities.TRANSPORT_WIFI) -> NetworkCapabilities.TRANSPORT_WIFI
                        hasTransport(NetworkCapabilities.TRANSPORT_CELLULAR) -> NetworkCapabilities.TRANSPORT_CELLULAR
                        else -> -1
                    }
                }
            } else {
                cm.run {
                    cm.activeNetworkInfo?.run {
                        result = when (type) {
                            ConnectivityManager.TYPE_WIFI -> ConnectivityManager.TYPE_WIFI
                            ConnectivityManager.TYPE_MOBILE -> ConnectivityManager.TYPE_MOBILE
                            ConnectivityManager.TYPE_VPN -> ConnectivityManager.TYPE_VPN
                            else -> -1
                        }
                    }
                }
            }
            return result != -1
        }
}