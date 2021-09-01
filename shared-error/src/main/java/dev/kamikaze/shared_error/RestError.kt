package dev.kamikaze.shared_error

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable

@Serializable
data class RestError(

    @SerialName("status_message")
    override var titleText: String? = "",

    override var subtitleText: String? = "",

    @SerialName("status_code")
    override var code: Int? = 0,

    override var httpCode: Int? = 0,

    override var btnName: String? = ""

) : ApiError