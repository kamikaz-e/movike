package dev.kamikaze.shared_error

import android.content.Context
import dev.kamikaze.shared_error.util.ConnectNetworkUtil
import kotlinx.serialization.ExperimentalSerializationApi
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json
import retrofit2.HttpException
import java.io.IOException

@ExperimentalSerializationApi
class ApiErrorFactory(
    private val context: Context
) {

    private val apiErrorList = hashMapOf(
        34 to R.string.resource_not_found,
        40 to R.string.nothing_to_update,
        42 to R.string.request_method_not_support_resource,
        43 to R.string.not_connect_to_server,
        44 to R.string.id_invalid,
        46 to R.string.api_undergoing_maintenance,
        47 to R.string.input_not_valid
    )

    private val defaultError = RestError(
        titleText = context.getString(R.string.unknown_server_error)
    )

    private val networkError
        get() = RestError(
            titleText = context.getString(R.string.network_error_title),
            subtitleText = context.getString(R.string.network_error_subtitle)
        )

    fun handleError(throwable: Throwable?): ApiError {
        return if (ConnectNetworkUtil(context).isConnected) {
            if (throwable is HttpException) {
                handleJsonError(throwable)
            } else {
                getError(throwable?.message)
            }
        } else {
            networkError
        }
    }

    private fun getError(errorString: String?) = RestError(
        titleText = errorString ?: context.getString(R.string.unknown_server_error)
    )

    private fun handleJsonError(httpException: HttpException): ApiError {
        return try {
            return parseApiError(httpException).apply {
                titleText = handleApiErrorCode(code)
                btnName = context.getString(R.string.update)
            }
        } catch (e: IOException) {
            defaultError
        }
    }

    private fun handleApiErrorCode(code: Int?): String {
        val stringError = apiErrorList[code] ?: R.string.unknown_server_error
        return context.getString(stringError)
    }

    private fun parseApiError(error: HttpException): RestError {
        val body = error.response()?.errorBody()?.string() ?: return defaultError
        return try {
            return Json.decodeFromString(body)
        } catch (ignored: IllegalStateException) {
            defaultError
        }
    }

}

