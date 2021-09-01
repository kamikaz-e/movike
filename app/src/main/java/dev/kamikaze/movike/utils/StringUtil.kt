package dev.kamikaze.movike.utils

import java.util.regex.Pattern

object StringUtil {

    private const val EMAIL_REGEX =
        "^[_A-Za-z0-9-]+(\\.[_A-Za-z0-9-]+)*@[A-Za-z0-9]+(\\.[A-Za-z0-9]+)*(\\.[A-Za-z]{2,})$"
    private const val IP_REGEX =
        "((25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9])\\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9]|0)\\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[1-9]|0)\\.(25[0-5]|2[0-4][0-9]|[0-1][0-9]{2}|[1-9][0-9]|[0-9]))"

    private const val DOT_CHAR = '.'
    private const val COMMA_CHAR = ','
    private const val ZERO_CHAR = '0'

    fun isExistNull(vararg arr: String?): Boolean {
        var isExistNull = true
        for (a in arr) {
            if (!(a.isNullOrBlank())) {
                isExistNull = false
                continue
            }
            isExistNull = true
            break
        }
        return isExistNull
    }

    fun isValidEmail(email: String) = Pattern.compile(EMAIL_REGEX).matcher(email).matches()

    fun isValidPhoneNumber(phoneNumber: String) = !isExistNull(phoneNumber)
            && (phoneNumber.length == 10 || phoneNumber.length == 11)

    fun isValidIpAddress(ipAddress: String) =
        !isExistNull(ipAddress) && ipAddress.matches(IP_REGEX.toRegex())

    fun getStringRoundingNumber(value: Float?, numberDigitsRound: Int): String? {
        val stringRoundValue = String.format("%.${numberDigitsRound}f", value).replaceCommaToDotChars()
        return handleFloatEmpty(stringRoundValue)
    }

    private fun String.replaceCommaToDotChars(): String {
        return replace(COMMA_CHAR, DOT_CHAR)
    }

    private fun handleFloatEmpty(value: String?): String? {
        return if (value?.toFloat() == 0f) null else value
    }

}