package dev.kamikaze.movike.utils

import java.text.SimpleDateFormat
import java.util.*

object DateUtil {

    fun getStringYear(dateString: String?): String {
        if (dateString.isNullOrEmpty()) return ""
        try {
            val oldFormat = SimpleDateFormat("yyy-MM-dd", Locale.ENGLISH)
            val newFormat = SimpleDateFormat("yyy", Locale.ENGLISH)
            val date = oldFormat.parse(dateString) ?: return ""
            val formattedString = newFormat.format(date)
            return (formattedString)
        } catch (e: Exception) {
            return ""
        }
    }

}