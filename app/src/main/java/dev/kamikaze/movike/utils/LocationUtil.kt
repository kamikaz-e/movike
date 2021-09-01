package dev.kamikaze.movike.utils

import android.content.Context
import android.location.LocationManager
import dev.kamikaze.movike.AppController

object LocationUtil {

    val isLocationAvailable: Boolean
        get() {
            val manager =
                AppController.appContext.getSystemService(Context.LOCATION_SERVICE) as LocationManager
            val isEnableGPS = manager.isProviderEnabled(LocationManager.GPS_PROVIDER)
            val isEnableNetwork = manager.isProviderEnabled(LocationManager.NETWORK_PROVIDER)
            return isEnableGPS || isEnableNetwork
        }
}